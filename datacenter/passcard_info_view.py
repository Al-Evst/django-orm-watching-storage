from datacenter.models import Passcard, Visit
from django.shortcuts import render, get_object_or_404
from django.utils.timezone import localtime, now


def visit_long(visit, threshold_seconds=3600):
    if visit.leaved_at:
        duration = visit.leaved_at - visit.entered_at
    else:
        duration = now() - visit.entered_at
    return duration.total_seconds() > threshold_seconds


def format_duration(duration):
    total_seconds = int(duration.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours}:{minutes:02d}:{seconds:02d}"


def passcard_info_view(request, passcode):
    passcard = get_object_or_404(Passcard, passcode=passcode)
    visits = Visit.objects.filter(passcard=passcard)

    threshold_seconds = 3600

    this_passcard_visits = []
    for visit in visits:
        entered_at_local = localtime(visit.entered_at).strftime('%d-%m-%Y %H:%M')

        if visit.leaved_at:
            duration = visit.leaved_at - visit.entered_at
        else:
            duration = now() - visit.entered_at

        duration_str = format_duration(duration)
        is_strange = "Да" if visit_long(visit, threshold_seconds) else "Нет"

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