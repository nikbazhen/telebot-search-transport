import requests
from config_data.config import KEY_API_SCHEDULE
from log import logger


def search_nearest_stations(longitude: str, latitude: str, name_transport: str) -> dict:
    """Функция для поиска ближайших станций по координатам пользователя"""
    logger.log_debug('Запуск функции search_nearest_stations')
    if name_transport == 'suburban':
        r = requests.get(
            f'https://api.rasp.yandex.net/v3.0/nearest_stations/?apikey={KEY_API_SCHEDULE}&format=json&lat={latitude}&lng={longitude}&distance=50&lang=ru_RU&transport_types=train')
        if r.status_code == 200:
            json_data = r.json()
            stations_dict = {}
            for i in json_data['stations']:
                stations_dict[i['title'][:30]] = [i["code"], i['title']]

            return stations_dict

    elif name_transport == 'train':
        r = requests.get(
            f'https://api.rasp.yandex.net/v3.0/nearest_stations/?apikey={KEY_API_SCHEDULE}&format=json&lat={latitude}&lng={longitude}&distance=50&lang=ru_RU&transport_types={name_transport}')
        if r.status_code == 200:
            json_data = r.json()
            stations_dict = {}
            for i in json_data['stations']:
                if i['majority'] == 1 or i['majority'] == 2:
                    stations_dict[i['title'][:30]] = [i["code"], i['title']]

            return stations_dict
    else:
        r = requests.get(
            f'https://api.rasp.yandex.net/v3.0/nearest_stations/?apikey={KEY_API_SCHEDULE}&format=json&lat={latitude}&lng={longitude}&distance=50&lang=ru_RU&transport_types={name_transport}')
        if r.status_code == 200:
            json_data = r.json()
            stations_dict = {}
            for i in json_data['stations']:
                stations_dict[i['title'][:30]] = [i["code"], i['title']]

            return stations_dict
