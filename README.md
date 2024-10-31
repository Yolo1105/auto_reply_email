# Automated HPC Question Drafting Tool

This project is designed to help instructors and support staff efficiently manage and respond to student inquiries related to High-Performance Computing (HPC). It automatically checks the inbox for incoming student emails, analyzes specific senders, and drafts responses for common questions. This automated system streamlines communication, especially when multiple students ask similar questions, allowing for faster and more organized responses.

## Features
- **Automatic Draft Creation**: Detects emails from specified student accounts and automatically drafts replies for HPC-related questions, saving time and ensuring consistency.
- **Gmail Integration**: Utilizes the Gmail API to access the inbox, filter for relevant questions, and draft responses.
- **Popup Notifications**: Notifies you upon successful draft creation.

## Prerequisites

### Requirements
- Python 3.x
- Google Cloud Platform (GCP) account with the Gmail API enabled
- `credentials.json` file for OAuth2 authentication
- A school-supported Gmail account

### Dependencies
The necessary Python libraries for this project are listed in `requirements.txt`. Install these dependencies with:
```bash
pip install -r requirements.txt
```

#### `requirements.txt` Contents
- `cryptography`: For encrypting and decrypting sensitive information like passwords.
- `keyring`: For securely storing sensitive data such as passwords on your operating system.
- `google-auth`, `google-auth-oauthlib`, `google-auth-httplib2`: For Google OAuth2 authentication.
- `google-api-python-client`: To interact with the Gmail API.

## Setting Up the Project

### Step 1: Create a GCP Project and Enable the Gmail API

Since your school-supported Gmail account requires two-factor authentication, we’ll use OAuth2 authentication to securely access the inbox. Here’s how to set up everything in Google Cloud Platform:

1. **Go to Google Cloud Console**:
   - Open [Google Cloud Console](https://console.cloud.google.com/).

2. **Create a New Project**:
   - In the Console, click on **Select a project** at the top and then **New Project**. Give your project a name and click **Create**.

3. **Enable the Gmail API**:
   - Go to **APIs & Services** > **Library**.
   - Search for “Gmail API” and click on it.
   - Click **Enable** to enable the Gmail API for this project.

4. **Set Up OAuth Consent Screen**:
   - Go to **APIs & Services** > **OAuth consent screen**.
   - Set the user type to **Internal** if you’re the only user or **External** if you plan to share it.
   - Fill out the necessary fields (e.g., App name, support email) and add `https://www.googleapis.com/auth/gmail.readonly`, `https://www.googleapis.com/auth/gmail.send`, and `https://www.googleapis.com/auth/gmail.modify` as scopes. These permissions allow the app to read, draft, and modify emails.

5. **Create OAuth Credentials**:
   - Go to **APIs & Services** > **Credentials**.
   - Click **Create Credentials** > **OAuth client ID**.
   - Choose **Desktop App** as the application type and give it a name.
   - Download the resulting `credentials.json` file and place it in your project directory.

### Step 2: Configure Keyring and Password Encryption

For security, this project uses `cryptography` to encrypt sensitive information, such as passwords.

1. **Encrypt the Password**:
   - Run the following Python code to securely encrypt your email password and save it:
     ```python
     from cryptography.fernet import Fernet
     import keyring

     # Generate a key for encryption
     decryption_key = Fernet.generate_key()
     keyring.set_password("email_service", "decryption_key", decryption_key.decode())

     # Encrypt the password
     cipher = Fernet(decryption_key)
     encrypted_password = cipher.encrypt(b"your_password_here")

     # Save encrypted password to a file
     with open("encrypted_password.bin", "wb") as file:
         file.write(encrypted_password)
     ```
   - Replace `your_password_here` with your email password.
   - After running this, you’ll have an `encrypted_password.bin` file containing your encrypted password and the decryption key securely stored in Keyring.

2. **Update the Project Script**:
   - In the main project script, `auto_reply.py`, the password will be automatically decrypted using Keyring.

### Step 3: Running the Project

1. Ensure the `credentials.json` file, `encrypted_password.bin` file, and your script are all in the same directory.
2. Run the script:
   ```bash
   python auto_reply.py
   ```

The script will:
1. Authenticate using OAuth2 via `credentials.json`.
2. Check for new emails in the inbox from specific student email addresses (e.g., `mohan.lu1105@gmail.com`).
3. Automatically draft a response for any emails that meet the conditions.
4. Display a popup notification when a draft is successfully created.

## Notes

- **Token Refresh**: The script will automatically refresh tokens if they expire. The first time you run it, you’ll be prompted to grant permissions in a browser.
- **Draft Mode**: This project only creates drafts and does not send emails, giving you a chance to review responses before sending them.

## Troubleshooting

### Common Issues

1. **OAuth Errors**:
   - If you see a "FileNotFoundError" for `credentials.json`, ensure it’s in the correct directory.
   - For "Insufficient Permission" errors, ensure you’ve deleted any existing `token.json` file, then re-run the script to re-authenticate with the updated scopes.

2. **Gmail API Quota Limits**:
   - The Gmail API has usage quotas. Avoid setting a very short interval for email checks to prevent hitting these limits.

3. **Missing or Incorrect Scopes**:
   - Make sure `https://www.googleapis.com/auth/gmail.readonly`, `https://www.googleapis.com/auth/gmail.send`, and `https://www.googleapis.com/auth/gmail.modify` are added to your app's OAuth consent screen and are specified in the Python script.

### Important Reminders

- **Security**: Do not share your `credentials.json` or `encrypted_password.bin` files. They contain sensitive information and should be kept secure.
- **Testing**: Always test the project in a safe environment to ensure it drafts messages correctly before using it in a production environment.

## Setting Up Automatic Startup

To ensure the script runs automatically when your computer starts, follow these simple steps to set up a startup shortcut:

### Steps to Run the Script at Startup with a Shortcut

1. **Create a Shortcut for the Script**:
   - Locate your Python script (`auto_reply.py`) or a batch file that runs it.
   - Right-click on the file, select **Create Shortcut**, and rename it (e.g., `AutoHPCResponder`).

2. **Move the Shortcut to the Startup Folder**:
   - Press `Win + R` to open the Run dialog.
   - Type `shell:startup` and press Enter to open the **Startup** folder.
   - Drag and drop the shortcut you created into this folder. Any program in the Startup folder will run automatically whenever your computer starts.

3. **Test the Setup**:
   - Restart your computer, and the script should automatically run on startup.

### Disabling the Startup Shortcut
To disable the script from running on startup, simply delete the shortcut from the **Startup** folder.

This method is straightforward and doesn’t require additional configuration. It’s a quick way to ensure the script runs in the background whenever you start your laptop.
