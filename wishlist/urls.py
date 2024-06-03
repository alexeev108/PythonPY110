from django.urls import path

from store.views import products_page_view
from .views import wishlist_remove_view, \
    wishlist_add_json, wishlist_del_json, wishlist_view, wishlist_page_json, wishlist_add_now_view

app_name = 'wishlist'

urlpatterns = [
    path('product/<slug:page>.html', products_page_view, name="products_page_view"),
    path('product/<int:page>', products_page_view),
    path('wishlist/', wishlist_view, name="wishlist_page_view"),
    path('wishlist/add/<str:id_product>', wishlist_add_now_view, name="wishlist_add_now"),
    path('wishlist/del/<str:id_product>', wishlist_remove_view, name="wishlist_remove_now"),
    path('wishlist/api/', wishlist_page_json, name="wishlist_json_page"),
    path('wishlist/api/add/<str:id_product>', wishlist_add_json, name="wishlist_json_add"),
    path('wishlist/api/del/<str:id_product>', wishlist_del_json, name="wishlist_json_remove"),
]