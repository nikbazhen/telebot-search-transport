import json
import requests
from config_data.config import KEY_API_SCHEDULE

# Код в файле используется для обновления станций/остановочных платформ. Рекомендуется запускать его раз в 6-12 месяцев.
r = requests.get(f"https://api.rasp.yandex.net/v3.0/stations_list/?apikey={KEY_API_SCHEDULE}&lang"
                 "=ru_RU&format=json")
if r.status_code == 200:
    json_dict = json.loads(r.text)
    with open('departure_points.json', 'w', encoding='utf-8') as file:
        json.dump(json_dict, file, indent=4, ensure_ascii=False)
else:
    raise Exception('Error connecting to the Yandex server')


with open('departure_points.json', 'r', encoding='utf-8') as file_departure_points:
    departure_dict = json.load(file_departure_points)
    data_rus_dict = departure_dict["countries"][29]["regions"]
    with open('result_codes.json', 'w', encoding='utf-8') as file_result_code:
        with open('codes_IATA.json', 'r', encoding='utf-8') as file_codes_IATA:
            codes_IATA_dict = json.load(file_codes_IATA)
            with open('codes_Russian_Railroads.json', 'r', encoding='utf-8') as file_codes_Russian_Railroads:
                codes_Russian_Railroads = json.load(file_codes_Russian_Railroads)
                codes = {}
                dict_city = {}
                dict_bus = {}
                dict_train = {}
                dict_plane = {}
                codes['city'] = [dict_city]
                codes['bus'] = [dict_bus]
                codes['train'] = [dict_train]
                codes['plane'] = [dict_plane]
                for i in data_rus_dict:
                    for x in i['settlements']:
                        if x.get("title"):
                            dict_city[x["title"].upper()] = x["codes"]["yandex_code"]
                for i in data_rus_dict:
                    for x in i['settlements']:
                        for y in x['stations']:
                            if y['transport_type'] == 'bus':
                                dict_bus[y["title"].upper()] = y["codes"]["yandex_code"]
                            elif y['transport_type'] == 'train':
                                dict_train[y["title"].upper()] = y["codes"]["yandex_code"]
                            elif y['transport_type'] == 'plane':
                                dict_plane[y["title"].upper()] = y["codes"]["yandex_code"]
                json.dump(codes, file_result_code, ensure_ascii=False, indent=4)
