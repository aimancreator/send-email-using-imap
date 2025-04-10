import imaplib
import smtplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# ---- Configuration (replace with your actual credentials) ----
EMAIL_ADDRESS = "youemail@domainname.com"  # Your email address
PASSWORD = "your password"           # Your email password or app password
SMTP_SERVER = "server name"          # Your SMTP server (e.g., "smtp.gmail.com")
SMTP_PORT = 587                           # Your SMTP port (e.g., 587 for TLS, 465 for SSL)

def send_email(recipient, subject, body, attachment_path=None):
    """
    Sends an email using SMTP with optional attachment.

    Args:
        recipient (str): Recipient's email address.
        subject (str): Email subject.
        body (str): Email body.
        attachment_path (str, optional): Path to the attachment file. Defaults to None.
    """

    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = recipient
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'html'))  # Use 'plain' or 'html' for body format

    if attachment_path:
        filename = attachment_path.split("/")[-1] # Get the filename from the path

        try:
            with open(attachment_path, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
        except FileNotFoundError:
            print(f"Error: Attachment file not found: {attachment_path}")
            return False # Indicate failure to send

        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename= {filename}")
        msg.attach(part)

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Upgrade connection to TLS
            server.login(EMAIL_ADDRESS, PASSWORD)
            server.sendmail(EMAIL_ADDRESS, recipient, msg.as_string())
        print(f"Email sent successfully to {recipient}")
        return True # Indicate success
    except Exception as e:
        print(f"Error sending email: {e}")
        return False # Indicate failure
# Example Usage

contenttext="""This is testing purposes """

send_email("receiver email", "Sell loklok", contenttext)
  