from django.urls import path

from store.views import products_view, shop_view, products_page_view, cart_view, cart_add_view, cart_del_all_view, \
    cart_del_one_view, coupon_check_view, delivery_estimate_view

app_name = 'store'

urlpatterns = [
    path('', shop_view),
    path('product/', products_view, name="shop_view"),
    path('product/<slug:page>.html', products_page_view, name="products_page_view"),
    path('product/<int:page>', products_page_view),
    path('cart/', cart_view, name="cart_page_view"),
    path('cart/add/<str:id_product>', cart_add_view),
    path('cart/del/<str:id_product>', cart_del_all_view),
    path('cart/del_one/<str:id_product>', cart_del_one_view),
    path('coupon/check/<slug:name_coupon>', coupon_check_view),
    path('delivery/estimate/', delivery_estimate_view),
]
