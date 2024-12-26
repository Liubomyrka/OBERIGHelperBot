# utils/calendar_utils.py

from google.oauth2 import service_account
from googleapiclient.discovery import build
import os
from datetime import datetime, timezone, timedelta

# Шлях до файлу облікових даних
CREDENTIALS_FILE = os.getenv("GOOGLE_CREDENTIALS")
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
