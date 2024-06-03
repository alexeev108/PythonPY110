from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound, JsonResponse
from django.shortcuts import render, redirect

import store
import wishlist
from logic.services import remove_from_wishlist_all, add_to_wishlist, view_in_wishlist


# Create your views here.

@login_required(login_url='login:login_view')
def wishlist_view(request) -> JsonResponse:
    if request.method == 'GET':
        current_user = get_user(request).username
        data = view_in_wishlist(request)[current_user]
        json_param = request.GET.get('format')
        if (json_param == 'JSON') and (json_param.lower() == 'json'):
            return JsonResponse(data, json_dumps_params={'ensure_ascii': False,
                                                         'indent': 4})
        else:
            products = []
            for product_id in data['products']:
                product = wishlist.models.DATABASE[product_id]
                products.append(product)
            context = {"products": products}
            return render(request, 'wishlist/wishlist.html', context)


@login_required(login_url='login:login_view')
def wishlist_page_json(request):
    """
    Просмотр всех продуктов в избранном для пользователя и возвращение этого в JSON
    """
    if request.method == "GET":
        current_user = get_user(request).username
        data = view_in_wishlist(request)[current_user]
        if data:
            return JsonResponse(data, json_dumps_params={'ensure_ascii': False,
                                                         'indent': 4})

        return JsonResponse(
                {"answer": "Пользователь не авторизирован"},
                                status=404,
                                json_dumps_params={'ensure_ascii': False}
        )

@login_required(login_url='login:login_view')
def wishlist_add_json(request, id_product) -> JsonResponse:
    """
    Добавление продукта в избранное и возвращение информации об успехе или неудаче в JSON
    """
    if request.method == 'GET':
        result = add_to_wishlist(request, id_product)
        if result:
            return JsonResponse(
                {"answer": "Продукт успешно добавлен в избранное"},
                json_dumps_params={'ensure_ascii': False}
            )
        else:
            return JsonResponse(
                {"answer": "Неудачное добавление в избранное"},
                                status=404,
                                json_dumps_params={'ensure_ascii': False}
            )

def wishlist_del_json(request, id_product):
    """
    Удаление продукта из избранного и возвращение информации об успехе или неудаче в JSON
    """
    if request.method == "GET":
        result = remove_from_wishlist_all(request, id_product)
        if result:
            return JsonResponse({"answer": "Продукт успешно удалён из избранного"},
                                json_dumps_params={'ensure_ascii': False})

        else:
            return JsonResponse({"answer": "Неудачное удаление из избранного"},
                            status=404,
                            json_dumps_params={'ensure_ascii': False})

@login_required(login_url='login:login_view')
def wishlist_add_now_view(request, id_product):
    if request.method == "GET":
        result = add_to_wishlist(request, id_product)
        if result:
            return redirect("store:shop_view")

        return HttpResponseNotFound("Неудачное добавление в избранное")

def wishlist_remove_view(request, id_product):
    if request.method == "GET":
        result = remove_from_wishlist_all(request, id_product)
        if result:
            return redirect("wishlist:wishlist_page_view")

        return HttpResponseNotFound("Неудачное удаление из корзины")