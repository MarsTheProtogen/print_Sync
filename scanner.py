import subprocess
import struct
import os
import logging
import shutil
import json

"""
Created by MarsTheProtogen
Licensed under the Polyform SBA license

This code provides a quick and dirty method to verify 3D file integrity and scan for malware using ClamAV.
Additional documentation for these functions can be found at:
https://github.com/MarsTheProtogen/3d_file_verification/tree/main
Redistributed under the PolyForm SBA license.
"""

# Configure logging to output to scanning.log
logging.basicConfig(filename="scanning.log", level=logging.INFO)


def clam_scan(filename, clamAV_path):
    """
    Run ClamAV on the specified file and return the parsed scan results.

    Parameters:
        filename (str): Path to the file to scan.
        clamAV_path (str): Path to the ClamAV executable (e.g., /usr/bin/clamscan).

    Returns:
        tuple: A tuple containing:
            - files (list): Parsed scan details for each file.
            - result (dict): Summary of scan results with numeric values where applicable.
    """
    clamscan_path = clamAV_path  # Example: "/usr/bin/clamscan"

    # Execute the ClamAV scan
    process = subprocess.run([clamscan_path, filename], capture_output=True, text=True)
    output = process.stdout

    SUMMARY = False
    files = []
    leftovers = []

    # Split output into lines
    lines = output.split("\n")

    # Parse the scan results
    for line in lines:
        if "SUMMARY" not in line and not SUMMARY:
            if line != "":
                files.append(line.split(":"))
        elif not SUMMARY:
            SUMMARY = True
        else:
            if line.strip() != "":
                leftovers.append(line)
    
    # Process summary lines into a dictionary
    leftovers = [line.split(":", 1) for line in leftovers]
    result = {line[0].strip("    "): line[1].strip() for line in leftovers}

    # Convert numeric strings to integers where applicable
    for key in result:
        if result[key].isdigit():
            result[key] = int(result[key])

    return files, result


def is_valid_binary_stl(file_path):
    """
    Validate a binary STL file's integrity by checking its header and triangle count.

    Parameters:
        file_path (str): Path to the binary STL file.
    
    Returns:
        tuple: (is_valid (bool), message (str), num_triangles (int))
            is_valid: True if the file is a valid binary STL file, False otherwise.
            message: A description of the validation result.
            num_triangles: Number of triangles in the file (0 if error).
    """
    try:
        file_size = os.path.getsize(file_path)

        with open(file_path, 'rb') as f:
            header = f.read(80)  # Read the 80-byte header
            num_triangles_data = f.read(4)  # Read the triangle count

            # Verify that triangle count data was read
            if len(num_triangles_data) < 4:
                return False, "Incomplete file: unable to read triangle count.", 0
            
            # Convert binary data to integer
            num_triangles = struct.unpack('<I', num_triangles_data)[0]
            
            # Calculate expected file size: header (84 bytes) + 50 bytes per triangle
            expected_size = 84 + num_triangles * 50
            if file_size == expected_size:
                return True, "Valid binary STL file.", num_triangles
            else:
                return False, f"Size mismatch: expected {expected_size} bytes, got {file_size} bytes.", 0
    except Exception as e:
        return False, f"Error processing file: {e}", 0


def is_valid_ascii_stl(file_path, extra_allowed_keywords=None):
    """
    Validate an ASCII STL file's structure and content.

    Checks include:
      - File is not empty.
      - Presence of required STL keywords within the first 4096 characters.
      - File starts with 'solid' and ends with 'endsolid'.
      - Correct count of facets and vertices.
      - Detection of any unrecognized keywords.

    Parameters:
        file_path (str): Path to the ASCII STL file.
        extra_allowed_keywords (list, optional): Additional allowed keywords.
    
    Returns:
        tuple: (is_valid (bool), message (str), num_facets (int))
            is_valid: True if valid, False otherwise.
            message: Description of the validation result.
            num_facets: Number of facets (0 if invalid or error).
    """
    valid = False
    message = ""
    unrecognized = set()

    try:
        file_size = os.path.getsize(file_path)
        if file_size == 0:
            message = "File is empty. "
            return False, message + str(unrecognized), 0

        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # Check for required keywords in the first 4096 characters
        first_chunk = content[:4096].lower()
        required_keywords = ["facet normal", "outer loop", "vertex", "endloop", "endfacet"]
        missing_keywords = [kw for kw in required_keywords if kw not in first_chunk]
        if missing_keywords:
            message = f"Missing keywords in the first chunk: {', '.join(missing_keywords)}"
            return False, message + str(unrecognized), 0

        lines = content.splitlines()
        if not lines:
            message = "File has no content. "
            return False, message + str(unrecognized), 0

        # Verify the file starts with 'solid' and ends with 'endsolid'
        if not lines[0].strip().lower().startswith('solid'):
            message = "File does not start with 'solid' keyword. "
            return False, message, unrecognized

        if not lines[-1].strip().lower().startswith('endsolid'):
            message = "File does not end with 'endsolid'. "
            return False, message + str(unrecognized), 0

        num_facets = 0
        num_vertices = 0
        inside_facet = False

        # Count facets and vertices in the file
        for line in lines:
            stripped = line.strip().lower()
            if stripped.startswith('facet normal'):
                num_facets += 1
                inside_facet = True
            elif stripped.startswith('vertex') and inside_facet:
                num_vertices += 1
            elif stripped.startswith('endfacet'):
                inside_facet = False

        if num_facets == 0:
            message = "No 'facet normal' keywords found; not a valid STL."
            return False, message + str(unrecognized), 0

        if num_vertices != num_facets * 3:
            message = f"Mismatch: Expected {num_facets * 3} vertices, found {num_vertices}."
            return False, message + str(unrecognized), 0

        message = f"Valid ASCII STL file with {num_facets} facets."
        valid = True

        # Set of recognized keywords (can be extended with extra_allowed_keywords)
        recognized_keywords = {"solid", "endsolid", "facet normal", "outer loop", "vertex", "endloop", "endfacet"}
        if extra_allowed_keywords:
            recognized_keywords.update(kw.lower() for kw in extra_allowed_keywords)

        # Scan for unrecognized keywords
        for line in lines:
            stripped = line.strip().lower()
            if not stripped:
                continue
            # Skip numeric data lines
            if stripped[0].isdigit() or stripped[0] in "-+.":
                continue
            tokens = stripped.split()
            token1 = tokens[0]
            token2 = " ".join(tokens[:2]) if len(tokens) >= 2 else token1
            if token1 not in recognized_keywords and token2 not in recognized_keywords:
                unrecognized.add(token1)

        return False, message + str(unrecognized), num_facets
    except Exception as e:
        message = f"Error processing file: {e}"
        return False, message, unrecognized


def is_valid_obj(file_path):
    """
    Validate the structure of an OBJ file by checking for typical OBJ keywords.

    Parameters:
        file_path (str): Path to the OBJ file.
    
    Returns:
        tuple: (is_valid (bool), message (str))
            is_valid: True if the file is valid, False otherwise.
            message: A description of the validation result.
    """
    try:
        file_size = os.path.getsize(file_path)
        if file_size == 0:
            return False, "File is empty."

        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()

        valid_keywords = ('o', '#', 'vn', 's', 'mtllib', 'f', 'vt', 'v', 'usemtl')
        # Look for at least one valid keyword in the file
        for line in lines:
            stripped = line.strip()
            if stripped and stripped.startswith(valid_keywords):
                return True, "Valid OBJ file structure detected."

        return False, "No valid OBJ keywords found. This may not be a valid OBJ file."
    except Exception as e:
        return False, f"Error processing file: {e}"


# Main routine: Check file integrity and move files for synchronization
# Note: this would be ran regularly using some sort of automation
if __name__ == '__main__':
    # Load configuration settings from JSON file
    with open('settings.json', 'r') as f:
        config = json.load(f)
        unscanned = config["UNSCANNED_DIR"]
        jail_dir = config["JAIL_DIR"]
        clam_dir = config["CLAM_AV_DIR"]
        sync_dir = config["SYNC_DIR"]

    # Get list of files from the unscanned directory
    files = os.listdir(unscanned)
    files = [os.path.join(unscanned, file) for file in files]

    file_format = None

    # Process each file in the unscanned directory
    for file_path in files:
        logging.info("ClamScan starting...")
        # Scan the file for viruses using ClamAV
        scan_files, result = clam_scan(file_path, clam_dir)
        logging.info("Clam scan done.")

        # Check if the file is infected
        if result.get("Infected files") == 1:
            logging.error(f"Infected file detected: {file_path}")
            # TODO: Move infected file to JAIL directory and send email warning
            continue

        # TODO: Check polygon count and limit the number of polygons allowed

        def move_to():
            """
            Move the file to the synchronization directory.
            """
            shutil.move(file_path, sync_dir)
            logging.info(f"Moved file {file_path} to {sync_dir}")

        # Validate file as binary STL
        valid, message, triangles = is_valid_binary_stl(file_path)
        if valid:
            logging.info(f"File {file_path} is a valid binary STL file with {triangles} triangles.")
            file_format = "STL"
            move_to()
            continue

        # Validate file as ASCII STL
        valid, message, triangles = is_valid_ascii_stl(file_path)
        if valid:
            logging.info(f"File {file_path} is a valid ASCII STL file with {triangles} triangles.")
            file_format = "STL"
            move_to()
            continue

        # Validate file as OBJ
        valid, message = is_valid_obj(file_path)
        if valid:
            logging.info(f"File {file_path} is a valid OBJ file.")
            file_format = "OBJ"
            logging.warning("No support for OBJ files at the moment.")
            move_to()
            continue

        logging.warning(f"File {file_path} is not a valid binary STL, ASCII STL, or OBJ file.")
