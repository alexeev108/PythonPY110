from django.contrib.auth import get_user
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect

import store.models
from logic.services import view_in_cart, add_to_cart, remove_from_cart_one, filtering_category, remove_from_cart_all


# Create your views here.

def products_view(request) -> JsonResponse:
    template_name = 'store/shop.html'
    if request.method == 'GET':
        product_id = request.GET.get('id')
        products = store.models.DATABASE.copy()
        data_to_return = JsonResponse(products,
                                      safe=False,
                                      json_dumps_params=
                                      {
                                          'indent': 4,
                                          'ensure_ascii': False
                                      }
                                      )
        if product_id:
            try:
                products = products[product_id]
                data_to_return = JsonResponse(products,
                                              safe=False,
                                              json_dumps_params=
                                              {
                                                  'indent': 4,
                                                  'ensure_ascii': False
                                              }
                                              )
            except:
                data_to_return = HttpResponseNotFound("Данного продукта нет в базе данных")
            return data_to_return

        category_key = request.GET.get('category')
        ordering_key = request.GET.get('ordering')
        if ordering_key:
            if request.GET.get('reverse') and request.GET.get('reverse').lower() == 'true':
                data = filtering_category(store.models.DATABASE.copy(),
                                                    category_key,
                                                    ordering_key,
                                                    True
                                                    )
            else:
                data = filtering_category(store.models.DATABASE.copy(),
                                                    category_key,
                                                    ordering_key
                                                    )
        else:
            data = filtering_category(store.models.DATABASE.copy(),
                                                category_key
                                                )
        return render(request, template_name, {"products": data, "category": category_key})

def shop_view(request) -> HttpResponse:
    template_name = 'store/shop.html'
    if request.method == 'GET':
        product_id = request.GET.get('id')
        products = store.models.DATABASE.copy()
        data_to_return = JsonResponse(products,
                                      safe=False,
                                      json_dumps_params=
                                      {
                                          'indent': 4,
                                          'ensure_ascii': False
                                      }
                                      )
        if product_id:
            try:
                products = products[product_id]
                data_to_return = JsonResponse(products,
                                              safe=False,
                                              json_dumps_params=
                                              {
                                                  'indent': 4,
                                                  'ensure_ascii': False
                                              }
                                              )
            except:
                data_to_return = HttpResponseNotFound("Данного продукта нет в базе данных")
            return data_to_return

        category_key = request.GET.get('category')
        ordering_key = request.GET.get('ordering')
        if ordering_key:
            if request.GET.get('reverse') and request.GET.get('reverse').lower() == 'true':
                data = filtering_category(store.models.DATABASE.copy(),
                                          category_key,
                                          ordering_key,
                                          True
                                          )
            else:
                data = filtering_category(store.models.DATABASE.copy(),
                                          category_key,
                                          ordering_key
                                          )
        else:
            data = filtering_category(store.models.DATABASE.copy(),
                                      category_key
                                      )
    return render(request, template_name, {"products": data, "category": category_key})

def same_product(dict_):
    empty = []
    for item_ in store.models.DATABASE.copy().values():
        if (dict_['category'] == item_['category']) and (dict_['html'] != item_['html']):
            empty.append(item_)
            # new_empty = empty[:5] #вернуть, если хочется выставить ограничение из 5 продуктов
    return empty

def products_page_view(request, page) -> HttpResponse:
    template_name = 'store/product.html'
    if request.method == "GET":
        if isinstance(page, str):
            for data in store.models.DATABASE.copy().values():
                if data['html'] == page:  # Если значение переданного параметра совпадает именем html файла
                    other = same_product(data)
                    data_to_return = render(request, template_name, {"product": data, "same": other})
                    break
                else:
                    data_to_return = HttpResponse('Страница не найдена!', status=404)
        elif isinstance(page, int):
            data = store.models.DATABASE.copy().get(str(page))
            if data:
                other = same_product(data)
                data_to_return = render(request, template_name, {"product": data, "same": other})
            else:
                data_to_return = HttpResponse('Страница не найдена!', status=404)
        return data_to_return

def cart_view(request) -> JsonResponse:
    if request.method == 'GET':
        current_user = get_user(request).username
        data = view_in_cart(request)[current_user]
        json_param = request.GET.get('format')
        if (json_param == 'JSON') and (json_param.lower() == 'json'):
            return JsonResponse(data, json_dumps_params={'ensure_ascii': False,
                                                         'indent': 4})
        else:
            products = []
            for product_id, quantity in data['products'].items():
                product = store.models.DATABASE[product_id]
                product["quantity"] = quantity
                product["price_total"] = f"{quantity * product['price_after']:.2f}"
                products.append(product)
            context = {"products": products}
            return render(request, 'store/cart.html', context)

def cart_add_view(request, id_product) -> JsonResponse:
    if request.method == 'GET':
        result = add_to_cart(request, id_product)
        if result:
            return JsonResponse(
                {"answer": "Продукт успешно добавлен в корзину"},
                json_dumps_params={'ensure_ascii': False}
            )
        else:
            return JsonResponse(
                {"answer": "Неудачное добавление в корзину"},
                                status=404,
                                json_dumps_params={'ensure_ascii': False}
            )

def cart_del_all_view(request, id_product):
    if request.method == "GET":
        result = remove_from_cart_all(request, id_product)
        if result:
            return JsonResponse({"answer": "Продукт успешно удалён из корзины"},
                                json_dumps_params={'ensure_ascii': False})

        else:
            return JsonResponse({"answer": "Неудачное удаление из корзины"},
                            status=404,
                            json_dumps_params={'ensure_ascii': False})

def cart_del_one_view(request, id_product):
    if request.method == "GET":
        result = remove_from_cart_one(request, id_product)
        if result:
            return JsonResponse({"answer": "1 позиция продукта успешно удалена из корзины"},
                                json_dumps_params={'ensure_ascii': False})

        else:
            return JsonResponse({"answer": "Неудачное удаление из корзины"},
                            status=404,
                            json_dumps_params={'ensure_ascii': False})

def coupon_check_view(request, name_coupon):
    DATA_COUPON = {
        "coupon": {
            "value": 10,
            "is_valid": True},
        "coupon_old": {
            "value": 20,
            "is_valid": False},
        "coupon_new": {
            "value": 30,
            "is_valid": True},
    }
    if request.method == "GET":
        if name_coupon and name_coupon in DATA_COUPON:
            return JsonResponse({"discount": DATA_COUPON[name_coupon]["value"],
                                 "is_valid": DATA_COUPON[name_coupon]["is_valid"]},
                                json_dumps_params={'ensure_ascii': False})
        else:
            return HttpResponseNotFound("Неверный купон")

def delivery_estimate_view(request):
    DATA_PRICE = {
        "Россия": {
            "Москва": {"price": 80},
            "Санкт-Петербург": {"price": 140},
            "fix_price": 100,
        },
    }
    if request.method == "GET":
        data = request.GET
        country = data.get('country')
        city = data.get('city')
        if country or city:
            try:
                error = DATA_PRICE[country]
                if (country in DATA_PRICE) and (city in DATA_PRICE[country]):
                    for item_ in DATA_PRICE[country].keys():
                        if item_ == city:
                            return JsonResponse({"price": DATA_PRICE[country][city]["price"]},
                                                json_dumps_params={'ensure_ascii': False})
                else:
                    return JsonResponse({"price": DATA_PRICE[country]["fix_price"]},
                                        json_dumps_params={'ensure_ascii': False})
            except:
                return HttpResponseNotFound("Неверные данные")
        else:
            return HttpResponseNotFound("Неверные данные")

def cart_buy_now_view(request, id_product):
    if request.method == "GET":
        result = add_to_cart(request, id_product)
        if result:
            return redirect("store:cart_page_view")

        return HttpResponseNotFound("Неудачное добавление в корзину")

def cart_remove_view(request, id_product):
    if request.method == "GET":
        result = remove_from_cart_all(request, id_product)
        if result:
            return redirect("store:cart_page_view")

        return HttpResponseNotFound("Неудачное удаление из корзины")