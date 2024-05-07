import json

import requests
from datetime import datetime

# Словарь перевода значений направления ветра
DIRECTION_TRANSFORM = {
    'n': 'северное',
    'nne': 'северо - северо - восточное',
    'ne': 'северо - восточное',
    'ene': 'восточно - северо - восточное',
    'e': 'восточное',
    'ese': 'восточно - юго - восточное',
    'se': 'юго - восточное',
    'sse': 'юго - юго - восточное',
    's': 'южное',
    'ssw': 'юго - юго - западное',
    'sw': 'юго - западное',
    'wsw': 'западно - юго - западное',
    'w': 'западное',
    'wnw': 'западно - северо - западное',
    'nw': 'северо - западное',
    'nnw': 'северо - северо - западное',
    'c': 'штиль',
}

# def current_weather_with_api_weather(lat,lon):
#     key = '0ba93e61c77a476c8d6104543240605'
#     url = 'http://api.weatherapi.com/v1/current.json'
#     params = {'key': key, 'q':f'{lat},{lon}'}
#     response = requests.get(url, params=params).json()
#     s = (f'Город: {response["location"]["name"]}\n'
#          f'Температура: {response["current"]["temp_c"]}\n'
#          f'Как ощущается: {response["current"]["feelslike_c"]}\n'
#          f'Ветер: {response["current"]["wind_kph"]}\n'
#          f'Время: {datetime.fromtimestamp(response["current"]["last_updated_epoch"])}')
#     return s

def current_weather(lat, lon):
    """
    Функция отправляет запрос GET на сайт https://api.weather.yandex.ru/v2/forecast
    и возвращает словарь в json формате с погодными условиями в городе
    :param lat: географическая широта расположения города
    :param lon: географическая долгота расположения города
    :return: словарь в json формате с погодными условиями в городе
    """
    token = '6ca4ce6a-34f4-4cf4-93c6-3692ffee23c2'  # Вставить ваш токен
    url = f"https://api.weather.yandex.ru/v2/forecast?lat={lat}&lon={lon}"  # Если вдруг используете тариф «Погода на вашем сайте»
    # то вместо forecast используйте informers. url = f"https://api.weather.yandex.ru/v2/informers?lat={lat}&lon={lon}"
    headers = {"X-Yandex-Weather-Key": f"{token}"}
    response = requests.get(url, headers=headers)
    data = response.json()

    # Данная реализация приведена для тарифа «Тестовый», если у вас Тариф «Погода на вашем сайте», то закомментируйте пару строк указанных ниже
    result = {
        'city': data['geo_object']['locality']['name'],  # Если используете Тариф «Погода на вашем сайте», то закомментируйте эту строку
        'time': datetime.fromtimestamp(data['fact']['uptime']).strftime("%H:%M"),  # Если используете Тариф «Погода на вашем сайте», то закомментируйте эту строку
        'temp': data['fact']['temp'],  # TODO Реализовать вычисление температуры из данных полученных от API
        'feels_like_temp': data['fact']['feels_like'],  # TODO Реализовать вычисление ощущаемой температуры из данных полученных от API
        'pressure': data['fact']['pressure_mm'],  # TODO Реализовать вычисление давления из данных полученных от API
        'humidity': data['fact']['humidity'],  # TODO Реализовать вычисление влажности из данных полученных от API
        'wind_speed': data['fact']['wind_speed'],  # TODO Реализовать вычисление скорости ветра из данных полученных от API
        'wind_gust': data['fact']['wind_gust'],  # TODO Реализовать вычисление скорости порывов ветка из данных полученных от API
        'wind_dir': DIRECTION_TRANSFORM.get(data['fact']['wind_dir']),  # Если используете Тариф «Погода на вашем сайте», то закомментируйте эту строку
    }
    return result


if __name__ == "__main__":
    print(current_weather(59.93, 30.31))  # Проверка работы для координат Санкт-Петербурга
