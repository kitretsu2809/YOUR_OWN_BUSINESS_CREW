from datetime import datetime, timedelta
from typing import Optional
from src.env import CALENDAR_API_KEY


def _generate_ics(title: str, start: datetime, end: datetime, description: Optional[str]) -> str:
    description_text = description or "Scheduled event."
    return (
        "BEGIN:VCALENDAR\n"
        "VERSION:2.0\n"
        "PRODID:-//YOUR_OWN_BUSINESS_CREW//EN\n"
        "BEGIN:VEVENT\n"
        f"SUMMARY:{title}\n"
        f"DTSTART:{start.strftime('%Y%m%dT%H%M%SZ')}\n"
        f"DTEND:{end.strftime('%Y%m%dT%H%M%SZ')}\n"
        f"DESCRIPTION:{description_text}\n"
        "END:VEVENT\n"
        "END:VCALENDAR\n"
    )


def create_event(title: str, start_timestamp: str, duration_minutes: int = 60, description: Optional[str] = None) -> str:
    start = datetime.fromisoformat(start_timestamp)
    end = start + timedelta(minutes=duration_minutes)

    if CALENDAR_API_KEY:
        # A calendar API key is available for future provider integration.
        # For now, we provide a standard ICS event payload that can be shared or imported into calendars.
        return _generate_ics(title, start, end, description)

    return _generate_ics(title, start, end, description)
