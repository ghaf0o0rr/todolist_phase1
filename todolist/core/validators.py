from __future__ import annotations
from datetime import datetime
from typing import Optional
from .errors import ValidationError
from .models import Status

MAX_NAME_LEN = 30
MAX_DESC_LEN = 150
VALID_STATUSES = {Status.TODO.value, Status.DOING.value, Status.DONE.value}

def validate_name(name: str) -> None:
    if not isinstance(name, str) or not name.strip():
        raise ValidationError("Name/title must be a non-empty string.")
    if len(name) > MAX_NAME_LEN:
        raise ValidationError(f"Name/title too long (>{MAX_NAME_LEN}).")

def validate_description(description: str) -> None:
    if description is None:
        return
    if len(description) > MAX_DESC_LEN:
        raise ValidationError(f"Description too long (>{MAX_DESC_LEN}).")

def validate_status(status: str) -> None:
    if status not in VALID_STATUSES:
        raise ValidationError(f"Invalid status '{status}'. Expected one of: {', '.join(sorted(VALID_STATUSES))}.")

def parse_deadline(deadline_str: Optional[str]):
    if deadline_str is None:
        return None
    try:
        return datetime.strptime(deadline_str, "%Y-%m-%d").date()
    except ValueError as e:
        raise ValidationError("Deadline must be in YYYY-MM-DD format.") from e
