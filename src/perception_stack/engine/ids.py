"""Identifier generation module"""

import uuid
from datetime import datetime, timezone


def generate_build_id(now: datetime | None = None) -> str:
    """
    Generates a chronologically sortable, unique identifier for a dataset build.

    Args:
        now: An optional timezone-aware datetime. If omitted, the current UTC time is used.
             Primarily exposed for dependency injection during testing.

    Returns:
        A unique, non-deterministic string formatted as `
         build_YYYYMMDDTHHMMSSZ_<12-char-hex>`.

    Raises:
        ValueError: If the provided datetime object is timezone-naive.
    """
    # Default to current UTC time if no timestamp is injected
    if now is None:
        now = datetime.now(timezone.utc)

    # Enforce timezone awareness to prevent subtle localization bugs in pipeline artifacts
    if now.tzinfo is None:
        raise ValueError("Build ID timestamp must be timezone-aware.")

    # Guarantee the timestamp is normalized to UTC before formatting
    now_utc = now.astimezone(timezone.utc)
    timestamp_str = now_utc.strftime("%Y%m%dT%H%M%SZ")

    # Use a 12-character hex string from a UUID4 to virtually eliminate collision risk
    random_hex = uuid.uuid4().hex[:12]

    return f"build_{timestamp_str}_{random_hex}"
