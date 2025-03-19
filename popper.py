# import required libraries

import os

# email tools
import poplib
import email
from email import policy
from email.message import EmailMessage
import smtplib

# debugging tools
import logging
import json

logging.basicConfig(filename="email.log", level=logging.DEBUG)

# put variables into scope
EMAIL_PASSWORD = None
ACCEPTED_FILES = None
SAVE_DIR = None
POP3_SERVER = None
EMAIL_ACCOUNT = None
SMTP_SERVER = None
SMTP_PORT = None

# load configuration from email.json
with open ('email.json') as json_file:
    config = json.load(json_file)
    EMAIL_PASSWORD = config["EMAIL_PASSWORD"]
    ACCEPTED_FILES = config["ACCEPTED_FILES"]
    SAVE_DIR = config["SAVE_DIR"]
    POP3_SERVER = config["POP3_SERVER"]
    EMAIL_ACCOUNT = config["EMAIL_ACCOUNT"]
    SMTP_SERVER = config["SMTP_SERVER"]
    SMTP_PORT = 465

    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)

def download_attachments():
    logging.info(f"Config loaded successfully: {config}")

    try:
        logging.info("[DEBUG] Connecting to POP3 server...")
        mailbox = poplib.POP3_SSL(POP3_SERVER)
        mailbox.user(EMAIL_ACCOUNT)
        mailbox.pass_(EMAIL_PASSWORD)
        logging.info("[DEBUG] Login successful!")

        # Get the number of messages
        num_messages = len(mailbox.list()[1])
        logging.info(f"[DEBUG] Number of emails found: {num_messages}")

        # Process the latest email (or iterate through all)
        for i in range(num_messages, max(num_messages - 5, 0), -1):  # Last 5 emails
            logging.info(f"[DEBUG] Fetching email #{i}...")
            response, lines, octets = mailbox.retr(i)  # Get email content
            raw_email = b"\n".join(lines)
            msg = email.message_from_bytes(raw_email, policy=policy.default)

            # Print Subject
            print(f"[DEBUG] Email Subject: {msg['Subject']}")

            # Check for attachments
            for part in msg.walk():
                if part.get_content_disposition() == "attachment":
                    filename = part.get_filename()
                    if filename:
                        logging.info(f"[DEBUG] Found attachment: {filename}")

                        # Save the attachment
                        file_path = os.path.join(SAVE_DIR, filename)

                        if filename.split(".")[1].lower() not in ACCEPTED_FILES:
                            logging.info(f"[DEBUG] Skipping non-3d or unsupported attachment: {filename} from: {msg['Subject']}")
                            continue


                        with open(file_path, "wb") as f:
                            f.write(part.get_payload(decode=True))

                        logging.info(f"[DEBUG] Saved attachment to: {file_path}")
                    else:
                        logging.info(f"[DEBUG] No attachment found.")

        # Close the connection
        mailbox.quit()
        logging.info("[DEBUG] Connection closed.")

    except Exception as e:
        logging.error(f"[ERROR] {e}")



def send_email(subject, body, to_email):
    """Send an email using SMTP."""
    try:
        msg = EmailMessage()
        msg["From"] = EMAIL_ACCOUNT
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.set_content(body)

        # Connect to SMTP server and send email
        print("[DEBUG] Connecting to SMTP server...")
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as smtp:  # Use SSL
            smtp.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
            print("[DEBUG] Logged into SMTP server.")
            smtp.send_message(msg)
            print(f"[DEBUG] Email sent to {to_email}!")

    except Exception as e:
        print(f"[ERROR] Failed to send email: {e}")


if __name__ == "__main__":
    send_email("New 3D Model Attachments", "Please find the new 3D model attachments attached.", "74lcheung@gmail.com")
