from flask import Flask, jsonify, request
import os
import logging

logging.basicConfig(filename='scanning.log', level=logging.INFO)
app = Flask(__name__)

@app.route('/scanned', methods=['GET', 'POST'])
def file_check():
    """
    Check if a file has been scanned and optionally remove it from the list.
    """

    # files that have been scanned
    # TODO re-scaning fs each time may need to be changed to periodic re-scanning
    scanned_files = os.listdir('SCANNED')
    scanned_files.remove("DONE") # remove DONE, is always a directory

    # clear files that have been processed (e.g., by the client)
    if request.method == 'POST':

        # Check if file exists and remove it if requested.
        incoming_data = request.get_json()
        remove = incoming_data['remove']

        # stores errors
        errors = []

        # handles file removal and error handling
        for _ in remove:
            try:
                # move file to DONE directory
                r = os.path.join('SCANNED', _)
                if os.path.isfile(r):
                    os.rename(r, os.path.join('SCANNED', 'DONE', _)) # rename to DONE directory)
                    logging.info(f"renaming {r} to DONE")
                
                # do nothing if file does not exist
                else:
                    logging.warning(f"file {_} does not exist")
            
                scanned_files.remove(_)  # remove the file from the list if requested

            except Exception as e:
                errors.append(str(e))

        if errors:
            return jsonify({'status': "error", 'errors': errors}), 400
        return jsonify({'status': "success"}), 200

    # Return a list of scanned files as JSON response.
    return jsonify({'scanned_files': scanned_files})



if __name__ == "__main__":
    app.run(host= "0.0.0.0", debug=True, port=5000)