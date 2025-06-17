from django.utils.timezone import now


SECONDS_IN_HOUR = 3600
SECONDS_IN_MINUTE = 60
LONG_VISIT_THRESHOLD_SECONDS = SECONDS_IN_HOUR  

def get_duration(visit):
    entered_at = visit.entered_at
    leaved_at = visit.leaved_at or now()
    return leaved_at - entered_at

def format_duration(duration):
    total_seconds = int(duration.total_seconds())
    hours, remainder = divmod(total_seconds, SECONDS_IN_HOUR)
    minutes, seconds = divmod(remainder, SECONDS_IN_MINUTE)
    return f"{hours}:{minutes:02d}:{seconds:02d}"

def is_visit_long(duration, threshold_seconds=LONG_VISIT_THRESHOLD_SECONDS):
    return duration.total_seconds() > threshold_seconds