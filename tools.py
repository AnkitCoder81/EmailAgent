# tools.py
from langchain_core.tools import tool
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64
from email.mime.text import MIMEText

@tool
def gmail_send(to: str, subject: str, message: str) -> str:
    """Send an email using the Gmail API."""
    try:
        creds = Credentials.from_authorized_user_file(
            "token.json",
            ["https://www.googleapis.com/auth/gmail.send"]
        )
        service = build("gmail", "v1", credentials=creds)

        mime_msg = MIMEText(message)
        mime_msg["to"] = to
        mime_msg["subject"] = subject
        raw_msg = base64.urlsafe_b64encode(mime_msg.as_bytes()).decode()

        message_body = {"raw": raw_msg}
        sent_msg = service.users().messages().send(
            userId="me",
            body=message_body
        ).execute()

        return f"Email sent to {to}. Message ID: {sent_msg['id']}"

    except HttpError as error:
        return f"An error occurred: {error}"
