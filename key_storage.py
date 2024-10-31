from cryptography.fernet import Fernet
import keyring

# Generate a key for encryption and save it in Keyring
decryption_key = Fernet.generate_key()
keyring.set_password("email_service", "decryption_key", decryption_key.decode())

# Encrypt the password and store it in a file
password = "Yolo!74847132"  # Replace this with your password only in this setup step
cipher = Fernet(decryption_key)
encrypted_password = cipher.encrypt(password.encode())

with open("encrypted_password.bin", "wb") as file:
    file.write(encrypted_password)
