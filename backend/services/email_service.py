import smtplib
from email.message import EmailMessage
from backend.config import EMAIL_ADDRESS, EMAIL_PASSWORD, ADMIN_EMAIL

def send_email(data):
    msg = EmailMessage()
    msg["Subject"] = "New Website Inquiry"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = ADMIN_EMAIL

    msg.set_content(f"""
Name: {data['name']}
Phone: {data['phone']}
Email: {data['email']}
Message: {data['message']}
""")

    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        raise ValueError("Email credentials not configured. Please set EMAIL_ADDRESS and EMAIL_PASSWORD in .env file.")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
