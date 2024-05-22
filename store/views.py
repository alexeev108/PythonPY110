from django.http import JsonResponse, HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render

import store.models
from logic.services import view_in_cart, add_to_cart, remove_from_cart_one, filtering_category, remove_from_cart_all


# Create your views here.

def products_view(request) -> JsonResponse:
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
        return JsonResponse(data, safe=False, json_dumps_params=
        {
            'indent': 4, 'ensure_ascii': False
        }
                            )

def shop_view(request) -> HttpResponse:
    if request.method == 'GET':
        with open('store/shop.html', 'r', encoding="utf-8") as file:
            data = file.read()
        return HttpResponse(data)

def products_page_view(request, page) -> HttpResponse:
    if request.method == "GET":
        if isinstance(page, str):
            for data in store.models.DATABASE.copy().values():
                if data['html'] == page:  # Если значение переданного параметра совпадает именем html файла
                    with open(f'store/products/{page}.html', 'r', encoding="utf-8") as f:
                        data_to_return = HttpResponse(f.read())
                        break
                else:
                    data_to_return = HttpResponse('Страница не найдена!', status=404)
        elif isinstance(page, int):
            data = store.models.DATABASE.copy().get(str(page))
            if data:
                with open(f'store/products/{data["html"]}.html', 'r', encoding="utf-8") as f:
                    data_to_return = HttpResponse(f.read())
            else:
                data_to_return = HttpResponse('Страница не найдена!', status=404)
        return data_to_return

def cart_view(request) -> JsonResponse:
    if request.method == 'GET':
        data = view_in_cart()
        return JsonResponse(data, safe=False, json_dumps_params=
        {
            'indent': 4, 'ensure_ascii': False
        }
                            )

def cart_add_view(request, id_product) -> JsonResponse:
    if request.method == 'GET':
        result = add_to_cart(id_product)
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
        result = remove_from_cart_all(id_product)
        if result:
            return JsonResponse({"answer": "Продукт успешно удалён из корзины"},
                                json_dumps_params={'ensure_ascii': False})

        else:
            return JsonResponse({"answer": "Неудачное удаление из корзины"},
                            status=404,
                            json_dumps_params={'ensure_ascii': False})

def cart_del_one_view(request, id_product):
    if request.method == "GET":
        result = remove_from_cart_one(id_product)
        if result:
            return JsonResponse({"answer": "1 позиция продукта успешно удалена из корзины"},
                                json_dumps_params={'ensure_ascii': False})

        else:
            return JsonResponse({"answer": "Неудачное удаление из корзины"},
                            status=404,
                            json_dumps_params={'ensure_ascii': False})