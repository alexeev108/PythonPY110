import datetime

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def datetime_view(requerst) -> HttpResponse:
    if requerst.method == 'GET':
        data = datetime.datetime.now()
        return HttpResponse(data.strftime('%H:%M %d/%m/%Y'))