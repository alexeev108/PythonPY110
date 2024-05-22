from django.urls import path

from store.views import products_view, shop_view
from app_weather.views import current_weather

urlpatterns = [
    path('weather/', current_weather)
]
