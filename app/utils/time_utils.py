"""Time utilities."""

from datetime import datetime, timedelta, timezone
from typing import Optional


def get_utc_now() -> datetime:
    """Get current UTC datetime."""
    return datetime.now(timezone.utc)


def parse_datetime(dt_string: str) -> Optional[datetime]:
    """Parse datetime string to datetime object."""
    try:
        return datetime.fromisoformat(dt_string.replace('Z', '+00:00'))
    except (ValueError, AttributeError):
        return None


def format_datetime(dt: datetime) -> str:
    """Format datetime to ISO string."""
    return dt.isoformat()


def add_timezone(dt: datetime, tz: timezone = timezone.utc) -> datetime:
    """Add timezone to naive datetime."""
    if dt.tzinfo is None:
        return dt.replace(tzinfo=tz)
    return dt


def get_next_scheduled_time(base_time: datetime, recurrence_pattern: str) -> Optional[datetime]:
    """Get next scheduled time based on recurrence pattern."""
    # TODO: Implement recurrence logic (daily, weekly, monthly, etc.)
    if recurrence_pattern == "daily":
        return base_time + timedelta(days=1)
    elif recurrence_pattern == "weekly":
        return base_time + timedelta(weeks=1)
    elif recurrence_pattern == "monthly":
        # Simplified monthly calculation
        return base_time + timedelta(days=30)
    
    return None

