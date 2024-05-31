import json
import os

from django.contrib.auth import get_user
from django.http import HttpResponseNotFound

import store.models


def filtering_category(database: dict[str, dict],
                       category_key: [None, str] = None,
                       ordering_key: [None, str] = None,
                       reverse: bool = False):
    """
    Функция фильтрации данных по параметрам

    :param database: База данных. (словарь словарей. При проверке в качестве database будет передаваться словарь DATABASE из models.py)
    :param category_key: [Опционально] Ключ для группировки категории. Если нет ключа, то рассматриваются все товары.
    :param ordering_key: [Опционально] Ключ по которому будет произведена сортировка результата.
    :param reverse: [Опционально] Выбор направления сортировки:
        False - сортировка по возрастанию;
        True - сортировка по убыванию.
    :return: list[dict] список товаров с их характеристиками, попавших под условия фильтрации. Если нет таких элементов,
    то возвращается пустой список
    """
    if category_key is not None:
        result = [product for product in store.models.DATABASE.copy().values() if product["category"] == category_key]  # TODO При помощи фильтрации в list comprehension профильтруйте товары по категории (ключ 'category') в продукте database. Или можете использовать
        # обычный цикл или функцию filter. Допустим фильтрацию в list comprehension можно сделать по следующему шаблону
        # [product for product in database.values() if ...] подумать, что за фильтрующее условие можно применить.
        # Сравните значение категории продукта со значением category_key
    else:
        result = list(store.models.DATABASE.copy().values())  # TODO Трансформируйте словарь словарей database в список словарей
        # В итоге должен быть [dict, dict, dict, ...], где dict - словарь продукта из database
    if ordering_key is not None:
        result.sort(key=lambda p: p[ordering_key], reverse=reverse)  # TODO Проведите сортировку result по ordering_key и параметру reverse
        # Так как result будет списком, то можно применить метод sort, но нужно определиться с тем по какому элементу сортируем и в каком направлении
        # result.sort(key=lambda ..., reverse=reverse)
        # Вспомните как можно сортировать по значениям словаря при помощи lambda функции
    return result

def view_in_cart(request) -> dict:
    if os.path.exists('cart.json'):
        with open('cart.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    user = get_user(request).username
    cart = {user: {'products': {}}}
    with open('cart.json', 'x',  encoding='utf-8') as f:
        json.dump(cart, f)
    return cart

def add_to_cart(request, id_product: str) -> bool:
    """
    Добавляет продукт в корзину. Если в корзине нет данного продукта, то добавляет его с количеством равное 1.
    Если в корзине есть такой продукт, то добавляет количеству данного продукта + 1.

    :param id_product: Идентификационный номер продукта в виде строки.
    :return: Возвращает True в случае успешного добавления, а False в случае неуспешного добавления(товара по id_product
    не существует).
    """
    cart_users = view_in_cart(request)
    cart = cart_users[get_user(request).username]
    products = store.models.DATABASE.copy()
    int_list = [int(item) for item in list(cart['products'].keys())]
    int_list_store = [int(item) for item in list(products.keys())]

    if int(id_product) not in int_list_store:
        result_bool = False
    else:
        if len(cart['products']) == 0:
            product_quantity = 1
            cart['products'][id_product] = product_quantity
        else:
            if int(id_product) not in int_list:
                product_quantity = 1
                cart['products'][id_product] = product_quantity
            else:
                for keys in list(cart['products'].keys()):
                    if int(keys) == int(id_product):
                        new = cart['products'][id_product]
                        new += 1
                        cart['products'][id_product] = new

        with open('cart.json', 'w', encoding='utf-8') as f:
            json.dump(cart_users, f)
            result_bool = True

    return result_bool

def remove_from_cart_all(request, id_product: str) -> bool:
    """
    Удаляет позицию продукта из корзины. Если в корзине есть такой продукт, то удаляется ключ в словаре
    с этим продуктом.

    :param id_product: Идентификационный номер продукта в виде строки.
    :return: Возвращает True в случае успешного удаления, а False в случае неуспешного удаления(товара по id_product
    не существует).
    """
    cart_users = view_in_cart(request)
    cart = cart_users[get_user(request).username]
    products = store.models.DATABASE.copy()
    int_list = [int(item) for item in list(cart['products'].keys())]
    int_list_store = [int(item) for item in list(products.keys())]

    if ((int(id_product) not in int_list_store) or
            (len(cart['products']) == 0) or
            (int(id_product) not in int_list)):
        result_bool = False
    else:
        for keys in list(cart['products'].keys()):
            if int(keys) == int(id_product):
                cart['products'].pop(id_product)

        with open('cart.json', 'w', encoding='utf-8') as f:
            json.dump(cart_users, f)
            result_bool = True

    return result_bool

def remove_from_cart_one(request, id_product: str) -> bool:
    """
    Удаляет продукт из корзины.
    Если в корзине есть такой продукт, то уменьшает количество данного продукта - 1.
    Если продукт присутствует в корзине в единственном количестве, то удаляет этот продукт.

    :param id_product: Идентификационный номер продукта в виде строки.
    :return: Возвращает True в случае успешного удаления, а False в случае неуспешного удаления(товара по id_product
    не существует).
    """
    cart_users = view_in_cart(request)
    cart = cart_users[get_user(request).username]
    products = store.models.DATABASE.copy()
    int_list = [int(item) for item in list(cart['products'].keys())]
    int_list_store = [int(item) for item in list(products.keys())]

    if ((int(id_product) not in int_list_store) or
            (len(cart['products']) == 0)):
        result_bool = False
    else:
        if cart['products'][id_product] == 1:
            cart['products'].pop(id_product)
        else:
            for keys in list(cart['products'].keys()):
                if int(keys) == int(id_product):
                    new = cart['products'][id_product]
                    new -= 1
                    cart['products'][id_product] = new

        with open('cart.json', 'w', encoding='utf-8') as f:
            json.dump(cart_users, f)
            result_bool = True

    return result_bool

def add_user_to_cart(request, username: str) -> None:
    """
       Добавляет пользователя в базу данных корзины, если его там не было.

       :param username: Имя пользователя
       :return: None
       """
    cart_users = view_in_cart(request)
    cart = cart_users.get(username)

    if not cart:
        with open('cart.json', mode='w', encoding='utf-8') as f:
            cart_users[username] = {'products': {}}
            json.dump(cart_users, f)

# if __name__ == "__main__":
#     # Проверка работоспособности функций view_in_cart, add_to_cart, remove_from_cart
#     # Для совпадения выходных значений перед запуском скрипта удаляйте появляющийся файл 'cart.json' в папке
#     print(view_in_cart())  # {'products': {}}
#     print(add_to_cart('1'))  # True
#     print(add_to_cart('0'))  # False
#     print(add_to_cart('1'))  # True
#     print(add_to_cart('2'))  # True
#     print(view_in_cart())  # {'products': {'1': 2, '2': 1}}
#     print(remove_from_cart('0'))  # False
#     print(remove_from_cart('1'))  # True
#     print(view_in_cart())  # {'products': {'2': 1}}