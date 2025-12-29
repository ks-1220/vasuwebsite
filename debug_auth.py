
import os
import smtplib
from dotenv import load_dotenv

# Force reload of .env
load_dotenv(override=True)

email = os.getenv("EMAIL_ADDRESS", "").strip()
password = os.getenv("EMAIL_PASSWORD", "").strip()

print(f"--- DEBUG INFO ---")
print(f"Email from .env: '{email}'")
if not email:
    print("[ERROR] EMAIL_ADDRESS is empty or missing in .env")

if password:
    print(f"Password from .env: {len(password)} characters long")
    print(f"Password starts with: {password[:2]}***{password[-2:]}")
else:
    print("[ERROR] EMAIL_PASSWORD is empty or missing in .env")

if not email or not password:
    print("Aborting due to missing credentials.")
    exit(1)

print(f"\nAttempting to connect to Gmail as {email}...")

try:
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.ehlo()
    print("[OK] Connected to Gmail SMTP server.")
    
    print("Attempting login...")
    server.login(email, password)
    print("[SUCCESS] Login credentials are correct.")
    server.quit()
except smtplib.SMTPAuthenticationError as e:
    print("[FAILED] AUTHENTICATION FAILED.")
    print("Expected reasons:")
    print("1. You are using your normal Gmail password instead of an APP PASSWORD.")
    print("2. You checked the wrong email address.")
    print("3. App Password copied incorrectly.")
    print(f"Server response: {e}")
except Exception as e:
    print(f"[ERROR] CONNECTION ERROR: {e}")
