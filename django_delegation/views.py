from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from .models import DelegatedView


def result(request, dg_id):
    dg_obj = get_object_or_404(DelegatedView, pk=dg_id)
    if dg_obj.finished:
        return redirect(dg_obj.data.url)

    return HttpResponse(u'<html><head><meta http-equiv="refresh" content="5"></head><body>Please be patient. Your page is loading... This page will refresh automatically every 5 seconds.</body></html>')
