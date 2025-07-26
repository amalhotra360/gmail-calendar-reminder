from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import datetime

SCOPES = ['https://www.googleapis.com/auth/calendar']

def authenticate_calendar():
    flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
    creds = flow.run_local_server(port=0)
    return build('calendar', 'v3', credentials=creds)

def add_event(service, summary, description, date_string):
    # Convert MM/DD/YYYY to ISO date
    month, day, year = map(int, date_string.split('/'))
    start_datetime = datetime.datetime(year, month, day, 9, 0)  # 9:00 AM
    end_datetime = start_datetime + datetime.timedelta(hours=1)

    event = {
        'summary': summary,
        'description': description,
        'start': {
            'dateTime': start_datetime.isoformat(),
            'timeZone': 'America/Los_Angeles',
        },
        'end': {
            'dateTime': end_datetime.isoformat(),
            'timeZone': 'America/Los_Angeles',
        },
    }

    event_result = service.events().insert(calendarId='primary', body=event).execute()
    print("✅ Event created:")
    print("📅 Summary:", event_result['summary'])
    print("🔗 Link:", event_result['htmlLink'])
