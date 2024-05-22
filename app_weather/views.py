from django.http import HttpResponse, JsonResponse
from django.shortcuts import render


import weather_api


# Create your views here.

def current_weather(request) -> JsonResponse:
    if request.method == 'GET':
        lat = request.GET.get('lat')
        lon = request.GET.get('lon')
        if lat and lon:
            data = weather_api.current_weather(lat=lat, lon=lon)
        else:
            data = weather_api.current_weather(59.93, 30.31)
        return JsonResponse(data, json_dumps_params={'ensure_ascii': False,
                                                     'indent': 4})