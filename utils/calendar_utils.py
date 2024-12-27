# utils/calendar_utils.py

from google.oauth2 import service_account
from googleapiclient.discovery import build
import os
from datetime import datetime, timezone, timedelta

# Шлях до файлу облікових даних
import os
CREDENTIALS_FILE = os.path.join(os.path.dirname(__file__), os.getenv("GOOGLE_CREDENTIALS"))
if not os.path.exists(CREDENTIALS_FILE):
    raise FileNotFoundError(f"❌ Файл облікових даних Google не знайдено за шляхом: {CREDENTIALS_FILE}")
CALENDAR_ID = os.getenv("CALENDAR_ID")


def get_calendar_events():
    credentials = service_account.Credentials.from_service_account_file(
        CREDENTIALS_FILE,
        scopes=["https://www.googleapis.com/auth/calendar.readonly"]
    )
    service = build("calendar", "v3", credentials=credentials)

    now = datetime.now(timezone.utc).isoformat()
    events_result = service.events().list(
        calendarId=CALENDAR_ID,
        timeMin=now,
        maxResults=10,
        singleEvents=True,
        orderBy="startTime"
    ).execute()

    return events_result.get("items", [])
