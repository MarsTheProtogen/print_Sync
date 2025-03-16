# py_talk Documentation v0.0.0

py_talk is a lightweight Python-based system designed to enhance the safety of automated downloads by acting as a disposable firewall. It is currently implemented for local machines and serves as an intermediary between receiving and processing common 3D printing files (such as STL and OBJ files) and more sensitive production environments. By isolating downloads and performing preliminary security checks, py_talk aims to prevent malware infections from propagating further.
Overview

In automated workflows, especially those involving files used in 3D printing or modeling, maintaining system integrity is critical. py_talk provides an extra layer of protection by:

### Scanning for Malware:
The server verifies files for malware and ensures that they match expected file types (e.g., STL, OBJ).
Isolation on Detection: Files suspected of containing malware are immediately moved to a designated JAIL directory, and an email warning is triggered.
Security Status Monitoring: In the event of a detected infection, the server either shuts down or updates its status via a dedicated endpoint (GET /status) to return {"secure": false}.
Intermediary Processing: Only files that pass these security checks are allowed to be downloaded and processed on the client side, keeping your sensitive systems protected.

# Why Use py_talk?

Enhanced Security:
Acts as a disposable firewall to prevent malware or infected files from reaching sensitive systems.

Automated Safety Checks:
Implements security measures to scan for malware and verify file types (focusing on common 3D printing formats) before processing.

Secure File Handling:
Uses secure protocols (SSH/SFTP) for file downloads and robust logging for troubleshooting.

Future-Ready Architecture:
Although the current implementation is for local machines, the design is modular enough to expand to decentralized systems in the future.

# Features

## REST API Server:
  ##### GET /scanned:
  Retrieves a JSON list of scanned files, excluding system directories like DONE or JAIL.
  
  ##### POST /scanned:
  Accepts a JSON payload to remove specified files from the scanned list, moving them to the appropriate directory (e.g., DONE for successfully processed files).
  
  ##### GET /status:
  Returns the current security status of the server. In the event of an infection, it will return {"secure": false}.
  

## Client Operations:
The py_talk class in client.py provides methods to:
    Retrieve the list of scanned files from the server.
    Remove files after processing (which triggers a move to the DONE directory).
    Download verified files securely from the server using SSH/SFTP.

## Security Checks & Isolation:
  Malware & File Type Verification:
  The server performs security checks to ensure each file is free from malware and conforms to expected 3D printing file formats (e.g., STL, OBJ).
  Quarantine on Threat Detection:
  Files detected as malware are moved to a JAIL directory, and an email notification is sent to alert administrators.
  Infection Handling:
  If a serious infection is detected, the server will either shut down or update its status via the GET /status endpoint to indicate that the system is no longer secure.

## Logging and Error Handling:
Detailed logs (stored in scanning.log) capture operations, errors, and security events for monitoring and debugging purposes.

# Current Implementation

Local Machine Deployment:
The system is designed for deployment on local machines. Both server and client components run within a local network environment.

3D Printing File Support:
The focus is on common 3D printing file formats such as STL and OBJ, ensuring that only verified and clean files are processed.

Disposable System as a Firewall:
Acts as an intermediary layer to prevent potentially infected files from reaching more sensitive environments.

# Future Enhancements

##### Detailed Security Checks:
Additional scanning capabilities and more comprehensive file integrity checks will be implemented to further safeguard against infections.

##### Email Integration:
Automated email alerts will be enhanced to provide real-time notifications on malware detections or other critical security events.

##### Decentralized System Support:
Although the current version is for local machines, future releases may expand to support decentralized environments.

##### No Web Dashboards Planned:
At this time, the focus is solely on backend processing and security; no web dashboards are planned for the near future.

# Installation & Setup

Clone the Repository:
Download or clone the repository containing server.py and client.py.

Install Dependencies:
Ensure Python 3.x is installed and install required libraries:

```pip install flask requests paramiko```

## Server Setup:

Create a directory named SCANNED on your machine.
Within SCANNED, create two subdirectories:
    DONE for processed files.
    JAIL for quarantined files in case of malware detection.
Start the Flask server:

```python server.py```

## Client Setup:

Create a settings.json file with configuration details:
```
{
"host": "your.server.address",
"port": 22,
"username": "your_username",
"key": "path/to/your/rsa_key.pem",
"SYNC_DIR": "/path/on/server/to/sync",
"DOWNLOAD_DIR": "/path/on/client/to/download"
}
```

Verify that the RSA key exists and the download directory is writable.
Run the client:

  ```python client.py```

# Usage
## Server API Endpoints

##### GET /scanned:
Returns a JSON list of scanned files (excluding DONE and JAIL directories).

##### POST /scanned:
Accepts a list of files:
```["filename1.stl", "filename2.obj"]```

  The server will move the specified files to the DONE directory if they are clean.

##### GET /status:
Returns the current security status:
    Normal operation: {"secure": true}.
    If an infection is detected: {"secure": false}.

## Client Methods

##### get_scanned_files():
Retrieves the list of scanned files from the server.

##### remove_scanned_file(filename):
Sends a request to remove a specific file from the scanned list, moving it to DONE.

##### download_scanned_file(files: list):
Establishes a secure SSH connection to download specified files from the server’s sync directory to the local download directory.

# Code Structure Overview

##### server.py:
Implements the Flask API to:
    Manage and track scanned files.
    Perform malware and file type checks.
    Isolate suspicious files by moving them to JAIL and sending email warnings.
    Update the security status via GET /status.

##### client.py:
Contains the py_talk class which:
    Loads configuration from settings.json.
    Communicates with the server to list, remove, and download scanned files.
    Uses Paramiko for secure file transfers via SSH/SFTP.
