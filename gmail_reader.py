from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import base64
import email
import re
from calendar_adder import authenticate_calendar, add_event


# Scopes let us read Gmail messages
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/calendar'
]

def authenticate_gmail():
    flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
    creds = flow.run_local_server(port=0)
    return build('gmail', 'v1', credentials=creds)

def read_emails_with_deadlines(service):
    results = service.users().messages().list(userId='me', q="deadline").execute()
    messages = results.get('messages', [])
    deadline_items = []

    for msg in messages[:5]:  # check only first 5 for now
        msg_data = service.users().messages().get(userId='me', id=msg['id']).execute()
        payload = msg_data['payload']
        headers = payload.get("headers")
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '')
        sender = next((h['value'] for h in headers if h['name'] == 'From'), '')

        parts = payload.get("parts", [])
        text = ""
        for part in parts:
            if part['mimeType'] == 'text/plain':
                data = part['body']['data']
                text = base64.urlsafe_b64decode(data).decode()

        match = re.search(r"deadline.*?(\d{1,2}/\d{1,2}/\d{4})", text, re.IGNORECASE)
        if match:
            deadline = match.group(1)
            deadline_items.append((subject, deadline, sender))

    return deadline_items

if __name__ == "__main__":
    gmail_service = authenticate_gmail()
    calendar_service = authenticate_calendar()
    
    emails = read_emails_with_deadlines(gmail_service)
    
    for subject, deadline, sender in emails:
        print(f"Subject: {subject}")
        print(f"Deadline: {deadline}")
        print(f"From: {sender}")
        print("---")
        
    add_event(
            service=calendar_service,
            summary=subject,
            description=f"Email from {sender}",
            date_string=deadline
        )
