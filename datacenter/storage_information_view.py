from django.shortcuts import render
from django.utils.timezone import localtime
from datacenter.models import Visit

from datacenter.utils import get_duration, format_duration, is_visit_long


def storage_information_view(request):
    active_visits = Visit.objects.filter(leaved_at__isnull=True)

    non_closed_visits = []
    for visit in active_visits:
        duration = get_duration(visit)
        formatted_duration = format_duration(duration)
        suspicious = is_visit_long(duration)

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