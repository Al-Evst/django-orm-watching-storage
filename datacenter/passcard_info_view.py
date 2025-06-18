from datacenter.models import Passcard, Visit
from django.shortcuts import render, get_object_or_404
from django.utils.timezone import localtime

from datacenter.utils import get_duration, format_duration, is_visit_long


def passcard_info_view(request, passcode):
    passcard = get_object_or_404(Passcard, passcode=passcode)
    visits = Visit.objects.filter(passcard=passcard)

    passcard_visits = []
    for visit in visits:
        entered_at = localtime(visit.entered_at).strftime('%d-%m-%Y %H:%M')
        duration = get_duration(visit)
        formatted_duration = format_duration(duration)
        suspicious = "Да" if is_visit_long(duration) else "Нет"

        passcard_visits.append({
            'entered_at': entered_at,
            'duration': formatted_duration,
            'is_strange': suspicious,
        })

    context = {
        'passcard': passcard,
        'this_passcard_visits': passcard_visits,
    }
    return render(request, 'passcard_info.html', context)
