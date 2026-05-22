from datetime import datetime, timezone


def is_within_buffer_time(timestamp_str, buffer_time_seconds):
    if buffer_time_seconds == 0.0:
        return False

    condition_time = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
    now = datetime.now(timezone.utc)
    elapsed = (now - condition_time).total_seconds()

    return buffer_time_seconds >= elapsed >= 0