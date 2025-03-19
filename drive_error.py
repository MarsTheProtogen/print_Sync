from popper import send_email
import json

google_drive_dir = None

# load configuration from email.json
with open ('email.json') as json_file:
    config = json.load(json_file)
    google_drive_dir = config["GOOGLE_DRIVE_DIR"]

subject = "Google drive sync error on server"
body = f"you likely need to re sign into rclone with 'rclone config reconnect {google_drive_dir}:'"

send_email()


