from django.http import JsonResponse, HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render

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
        data = view_in_cart()
        template_name = 'store/cart.html'
        json_param = request.GET.get('format')
        if (json_param == 'JSON') and (json_param.lower() == 'json'):
            return JsonResponse(data, json_dumps_params={'ensure_ascii': False,
                                                         'indent': 4})
        else:
            products = []
            for product_id, quantity in data['products'].items():
                product = store.models.DATABASE[product_id]
                product["price_total"] = f"{quantity * product['price_after']:.2f}"
                products.append(product)
            context = {"products": products}
            return render(request, template_name, context)

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