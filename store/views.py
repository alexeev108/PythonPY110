from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

import store.models


# Create your views here.

def products_view(request) -> JsonResponse:
    if request.method == 'GET':
        data = store.models.DATABASE
        return JsonResponse(data, json_dumps_params={'ensure_ascii': False,
                                                     'indent': 4})
def shop_view(request) -> HttpResponse:
    if request.method == 'GET':
        with open('store/shop.html', 'r', encoding="utf-8") as file:
            data = file.read()
        return HttpResponse(data)