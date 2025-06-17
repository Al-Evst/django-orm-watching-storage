from datacenter.models import Passcard, Visit
from django.shortcuts import render, get_object_or_404
from django.utils.timezone import localtime

from datacenter.utils import get_duration, format_duration, is_visit_long


def passcard_info_view(request, passcode):
    passcard = get_object_or_404(Passcard, passcode=passcode)
    visits = Visit.objects.filter(passcard=passcard)

    this_passcard_visits = []
    for visit in visits:
        entered_at_local = localtime(visit.entered_at).strftime('%d-%m-%Y %H:%M')
        duration = get_duration(visit)
        duration_str = format_duration(duration)
        is_strange = "Да" if is_visit_long(duration) else "Нет"

        this_passcard_visits.append({
            'entered_at': entered_at_local,
            'duration': duration_str,
            'is_strange': is_strange,
        })

    context = {
        'passcard': passcard,
        'this_passcard_visits': this_passcard_visits,
    }
    return render(request, 'passcard_info.html', context)