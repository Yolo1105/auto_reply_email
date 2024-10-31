import os
import ctypes
import time
import base64
import keyring
from cryptography.fernet import Fernet
from email.message import EmailMessage
from email.header import decode_header
import google.auth
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError

# Updated sender email and scopes
EMAIL = "ml7612@nyu.edu"  # This is the email used to send drafts
TRIGGER_EMAIL = "mohan.lu1105@gmail.com"  # The email address that triggers the draft creation
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/gmail.modify'
]

# Keep track of processed message IDs
processed_messages = set()

# Load the decryption key from Keyring and decrypt the password
decryption_key = keyring.get_password("email_service", "decryption_key").encode()
cipher = Fernet(decryption_key)

with open("encrypted_password.bin", "rb") as file:
    encrypted_password = file.read()

PASSWORD = cipher.decrypt(encrypted_password).decode()

# OAuth2 Authentication
def authenticate():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(google.auth.transport.requests.Request())
        else:
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

# Gmail API Service Setup
def get_gmail_service():
    creds = authenticate()
    return build('gmail', 'v1', credentials=creds)

def save_draft(service):
    try:
        message = EmailMessage()
        message["From"] = EMAIL
        message["To"] = TRIGGER_EMAIL
        message["Subject"] = "Test Draft"
        message.set_content("Hello, this draft was successfully created.")

        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        draft_body = {'message': {'raw': raw_message}}

        # Create the draft
        draft = service.users().drafts().create(userId='me', body=draft_body).execute()
        print("Draft created successfully.")
        
        # Show a pop-up to confirm draft creation
        ctypes.windll.user32.MessageBoxW(0, "Draft created successfully.", "Draft Notification", 1)
    except HttpError as error:
        print(f"An error occurred while creating draft: {error}")

def show_popup_notification(subject):
    ctypes.windll.user32.MessageBoxW(0, f"New Email from {TRIGGER_EMAIL}: {subject}", "Email Notification", 1)

def check_new_email():
    service = get_gmail_service()

    # List recent 50 messages in the inbox
    results = service.users().messages().list(userId='me', labelIds=['INBOX'], maxResults=50).execute()
    messages = results.get('messages', [])
    print(f"Found {len(messages)} messages in the inbox.")

    for msg in messages:
        msg_id = msg['id']

        # Skip if this message was already processed
        if msg_id in processed_messages:
            continue

        # Mark this message as processed
        processed_messages.add(msg_id)

        # Get the message details
        msg = service.users().messages().get(userId='me', id=msg_id).execute()
        headers = msg['payload']['headers']
        
        # Retrieve email details
        subject = ""
        from_email = ""
        for header in headers:
            if header['name'] == 'Subject':
                subject = header['value']
            elif header['name'] == 'From':
                from_email = header['value']
        
        print(f"Processing email from: {from_email}, subject: {subject}")

        # Check if the email is from the trigger email address
        if TRIGGER_EMAIL in from_email:
            print(f"Email from {TRIGGER_EMAIL} detected. Creating draft.")
            # Show pop-up for the new email only if it’s from the specified trigger address
            show_popup_notification(subject)

            # Create a draft instead of sending a reply
            save_draft(service)

            # Optionally mark email as read (remove 'UNREAD' label)
            service.users().messages().modify(userId='me', id=msg_id, body={'removeLabelIds': ['UNREAD']}).execute()
        else:
            print("Email is not from the trigger email. Skipping.")

# Periodically check for new emails
while True:
    try:
        check_new_email()
    except HttpError as error:
        print(f"An error occurred: {error}")
    time.sleep(60)  # Check every minute
