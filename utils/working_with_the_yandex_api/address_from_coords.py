import requests
from config_data.config import KEY_API_GEOLOCATION
from log import logger


def get_address(longitude_or_contry: str, latitude=None) -> (str, list):
    """Функция для поиска населённого пункта по координатам или координат по названию населённого пункта."""
    logger.log_debug('Запуск функции get_address')
    if longitude_or_contry.isdigit() or longitude_or_contry[:2].isdigit() or (longitude_or_contry[1:3].isdigit() and longitude_or_contry[0] == '-'):
        r = requests.get(f"https://geocode-maps.yandex.ru/1.x/?apikey={KEY_API_GEOLOCATION}&geocode={longitude_or_contry},{latitude}&kind=locality&results=1&format=json")
        if r.status_code == 200:
            json_data = r.json()
            address_str = json_data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["AddressDetails"]["Country"]["AddressLine"]
            return address_str
        else:
            raise Exception('Error connecting to the Yandex server')
    else:
        r = requests.get(f"https://geocode-maps.yandex.ru/1.x/?apikey={KEY_API_GEOLOCATION}&geocode={longitude_or_contry}&kind=locality&results=1&format=json")
        if r.status_code == 200:
            json_data = r.json()
            if len(json_data['response']["GeoObjectCollection"]['featureMember']) == 1:
                if json_data['response']["GeoObjectCollection"]['featureMember'][0]["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]['Address']['Components'][0]['name'] != 'Россия':
                    return [False, ('Этот бот работает только по населённым пунктам России, а введённая вами местоположение,'
                            ' не входит в состав России. Если это ошибка и если вы используйте Telegram с помощью ПК, '
                            'напишите ваше местоположение более точнее.\n'
                            'Пример точного местоположение города Москва - '
                            'Россия, Московская область, город Москва.\n'
                            'Если вы пользуетесь мобильным устройством, '
                            'будет намного проще нажать на кнопку "Поделиться местоположением" ')]
                elif len(json_data['response']["GeoObjectCollection"]['featureMember'][0]["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]['Address']['Components']) == 1:
                    return [False, ('Не найдено ни одного результата. Скорее всего вы допустили ошибку.'
                            ' Проверте введённое вами ваше место положение и повторите попытку.\n'
                            'Если вы используйте Telegram с помощью ПК, напишите ваше местоположение более точнее.\n'
                            'Пример точного местоположение города Москва - Россия, Московская область, город Москва.\n'
                            'Если вы пользуетесь мобильным устройством, '
                            'будет намного проще нажать на кнопку "Поделиться местоположением"')]
                else:
                    location_list = json_data['response']["GeoObjectCollection"]['featureMember'][0]['GeoObject']['Point']['pos']
                    address_str = json_data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["AddressDetails"]["Country"]["AddressLine"]
                    return [address_str, location_list.split(' ')]
            else:
                return [False, ('Найдено несколько совпадений по вашим введённым данным.\n'
                        'Если вы используйте Telegram с помощью ПК, напишите ваше местоположение более точнее.\n'
                        'Пример точного местоположение города Москва - Россия, Московская область, город Москва.\n'
                        'Если вы пользуетесь мобильным устройством, '
                        'будет намного проще нажать на кнопку "Поделиться местоположением"')]

        else:
            raise Exception('Error connecting to the Yandex server')
