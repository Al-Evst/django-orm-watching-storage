from django.shortcuts import render
from django.utils.timezone import localtime, now
from datacenter.models import Visit


def get_duration(visit):
    entered_at = visit.entered_at
    leaved_at = visit.leaved_at or now()
    return leaved_at - entered_at


def format_duration(duration):
    total_seconds = int(duration.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    return f"{hours}ч {minutes}мин"


def visit_suspicious(duration, threshold_minutes=60):
    return duration.total_seconds() > threshold_minutes * 60


def storage_information_view(request):
    active_visits = Visit.objects.filter(leaved_at__isnull=True)

    non_closed_visits = []
    for visit in active_visits:
        duration = get_duration(visit)
        formatted_duration = format_duration(duration)
        suspicious = visit_suspicious(duration)

        non_closed_visits.append({
            'who_entered': visit.passcard.owner_name,
            'entered_at': localtime(visit.entered_at),
            'duration_str': formatted_duration,
            'is_strange': suspicious,
        })

    context = {
        'non_closed_visits': non_closed_visits,
    }
    return render(request, 'storage_information.html', context)