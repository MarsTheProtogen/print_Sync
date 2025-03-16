import requests
import logging
import paramiko
import json
import os

class py_talk:
    def __init__(self):

        # logging configuration for non interactive
        logging.basicConfig(filename='scanning.log', level=logging.INFO)

        self.settings = "settings.json"

        self.hostname = None
        self.port = None
        self.username = None
        self.rsa_key_path = None
        self.SYNC_path = None
        self.DOWNLOAD_path = None

        """
        Configuration variables
        """
        try:
            with open(self.settings, "r") as file:
                f = json.load(file)
                self.hostname = f['host']
                self.port = f['port']
                self.username = f['username']
                self.rsa_key_path = f['key']
                self.SYNC_path = f['SYNC_DIR']
                self.DOWNLOAD_path = f['DOWNLOAD_DIR']

        except FileNotFoundError:
            print("Error: settings.json file not found.")
        except json.JSONDecodeError as err:
            print("Error decoding JSON:", err)
        
        # flask server url
        self.url = f'http://{self.hostname}'

        # check file paths
        if not os.path.exists(self.rsa_key_path):
            raise FileNotFoundError(f"RSA key file not found: {self.rsa_key_path}")
        
        if not os.path.exists(self.DOWNLOAD_path):
            os.makedirs(self.DOWNLOAD_path, exist_ok=True)

    def get_scanned_files(self):
        
        """
        get list of scanned files from the server
        """
        print("Getting scanned files from server...")
        response = requests.get(f'{self.url}/scanned')
        return response

    def remove_scanned_file(self, filename)-> str:
        """
        remove a file from the server's list of scanned files
        """
        
        # data to be sent to flask server
        data = {'remove': [filename]}

        # check response status code
        response = requests.post(f'{self.url}/scanned', json=data)

        # log warnings if not being ran directly.
        if not __name__ == "__main__":
            if response.status_code == 400:
                logging.error(f"Failed to move file: {filename} to DONE: {response.json()['errors']}")
                return "failed"
            elif response.status_code == 200:
                logging.info(f"Moved file: {filename} to DONE")
                return "success"
            else:
                logging.error(f"Failed to remove file: {filename} - unknown status code: {response.status_code}")
                return "failed"
            
        # if running directly, print the response
        else:
            if response.status_code == 400:
                print(f"Failed to remove file: {filename} - {response.json()['errors']}")
                return "failed"
            elif response.status_code == 200:
                print(f"Removed file: {filename}")
                return "success"
            else:
                print(f"Failed to remove file: {filename} - unknown status code: {response.status_code}")
                return "failed"


    def download_scanned_file(self, files:list):

        """
        download files from the server to the processing machine
        """

        # check if files is a list instead of a single file name
        if not type(files) == list:
            raise ValueError(f"file input needs to be a list, not {type(files).__name__}")


        """
        custom error handling for the SSH connection,

        will log the error if not being ran directly.
        """
        class InteractiveMissingHostKeyPolicy(paramiko.MissingHostKeyPolicy):
            
            # This policy will ask the user if they trust the host key if being ran directly
            if __name__ == "__main__":
                def missing_host_key(self, client, hostname, key):
                    fingerprint = key.get_fingerprint().hex()
                    print(f"Warning: The host '{hostname}' is not in your known hosts list.")
                    print(f"Host key type: {key.get_name()}")
                    print(f"Fingerprint: {fingerprint}")
                    response = input("Do you trust this host? (yes/no): ").strip().lower()
                    if response == "yes":
                        # Add the key to the host keys for future use.
                        client.get_host_keys().add(hostname, key.get_name(), key)
                        print("Host key added to known hosts.")
                    else:
                        raise paramiko.SSHException("Host key not trusted by user.")
            
            # bounce server key by default
            else:
                def missing_host_key(self, client, hostname, key):
                    logging.error(f"Failed to connect to {hostname}: Host key not accepted by default")
                    raise paramiko.SSHException("Host key not accepted by user.")

        # Create an SSH client instance
        client = paramiko.SSHClient()
        # Load system host keys if available
        client.load_system_host_keys()
        # Set our custom policy instead of automatically accepting host keys
        client.set_missing_host_key_policy(InteractiveMissingHostKeyPolicy())

        """
        attempts to connect to the remote server and download files
        """
        try:
            
            # Load RSA private key
            key = paramiko.RSAKey.from_private_key_file(self.rsa_key_path)

            # Connect to the remote server using RSA key authentication
            client.connect(self.hostname, port=self.port, username=self.username, pkey=key)
            if __name__ == "__main__":
                (f"Connected to {self.hostname} successfully.")
            else:
                logging.log(f"Connected to {self.hostname} successfully.")

            # Open an SFTP session on the SSH server
            sftp = client.open_sftp()

            # Download files from the server to the processing machine
            for _ in files:
                remote_file = os.path.join(self.SYNC_path, _)
                local_file = os.path.join(self.DOWNLOAD_path, _)

                # Download the file from the remote server
                sftp.get(remote_file, local_file)
                logging.info(f"Downloaded file: {remote_file} to {local_file}")

            # Close the SFTP session and SSH connection
            sftp.close()
            client.close()
            logging.info("SFTP session and SSH connection closed.")


        except paramiko.AuthenticationException as auth_err:
            if __name__ == "__main__":
                print("Authentication failed:", auth_err)
            else:
                logging.error("Authentication failed:", auth_err)
            return
        
        except paramiko.SSHException as ssh_err:
            if __name__ == "__main__":
                print("SSH error:", ssh_err)
            else:
                logging.error("SSH error:", ssh_err)
            return
        
        except FileNotFoundError as fnf_err:
            if __name__ == "__main__":
                print("file not found:", fnf_err)
            else:
                logging.error("file not found:", fnf_err)
            return
        
        except Exception as e:
            if __name__ == "__main__":
                print("An unexpected error occurred:", e)
            else:
                logging.error("An unexpected error occurred:", e)
            return
            
        finally:
            # Always ensure the SSH connection is closed even if an exception occurred
            client.close()

if __name__ == "__main__":
    c = py_talk()
    print("starting")
    print(c.get_scanned_files())