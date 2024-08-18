import json
import os
from log import logger


def check_codes_yandex(name_station: str, transport_type: str) -> (list, str, bool):
    """Функция для проверки названия населённого пункта или станции/остановочной платформы"""
    logger.log_debug('Запуск функции check_codes_yandex')
    text_upper = name_station.upper()
    with open(os.path.join('utils', 'working_with_the_yandex_api', 'result_codes.json'), 'r', encoding='utf-8') as file:
        convert_result_codes = json.load(file)
        if transport_type == 'plane':
            if convert_result_codes['plane'][0].get(text_upper) and convert_result_codes['city'][0].get(text_upper):
                return [None, f'Аэропорт {text_upper.title()}', f'Населённый пункт {text_upper.title()}']

            elif convert_result_codes['plane'][0].get(text_upper):
                return convert_result_codes['plane'][0][text_upper]
            elif text_upper.startswith('АЭРОПОРТ ') and convert_result_codes['plane'][0].get(text_upper[9:]):
                return convert_result_codes['plane'][0][text_upper[9:]]

            elif convert_result_codes['city'][0].get(text_upper):
                return convert_result_codes['city'][0][text_upper]
            elif text_upper.startswith('НАСЕЛЁННЫЙ ПУНКТ ') and convert_result_codes['city'][0].get(text_upper[17:]):
                return convert_result_codes['city'][0][text_upper[17:]]

            else:
                return False

        elif transport_type == 'bus':
            if convert_result_codes['bus'][0].get(text_upper) and convert_result_codes['city'][0].get(text_upper):
                return [None, f'Автобусная остановка {text_upper.title()}', f'Населённый пункт {text_upper.title()}']

            elif convert_result_codes['bus'][0].get(text_upper):
                return convert_result_codes['bus'][0][text_upper]
            elif text_upper.startswith('АВТОБУСНАЯ ОСТАНОВКА ') and convert_result_codes['bus'][0].get(
                    text_upper[21:]):
                return convert_result_codes['bus'][0][text_upper[21:]]

            elif convert_result_codes['city'][0].get(text_upper):
                return convert_result_codes['city'][0][text_upper]
            elif text_upper.startswith('НАСЕЛЁННЫЙ ПУНКТ ') and convert_result_codes['city'][0].get(text_upper[17:]):
                return convert_result_codes['city'][0][text_upper[17:]]

            else:
                return False
        elif transport_type == 'train' or transport_type == 'suburban':
            if convert_result_codes['train'][0].get(text_upper) and convert_result_codes['city'][0].get(text_upper):
                return [None, f'Станция {text_upper.title()}', f'Населённый пункт {text_upper.title()}']

            elif convert_result_codes['train'][0].get(text_upper) :
                return convert_result_codes['train'][0][text_upper]
            elif text_upper.startswith('СТАНЦИЯ ') and convert_result_codes['train'][0].get(text_upper[8:]):
                return convert_result_codes['train'][0][text_upper[8:]]

            elif convert_result_codes['city'][0].get(text_upper):
                return convert_result_codes['city'][0][text_upper]
            elif text_upper.startswith('НАСЕЛЁННЫЙ ПУНКТ ') and convert_result_codes['city'][0].get(text_upper[17:]):
                return convert_result_codes['city'][0][text_upper[17:]]

            else:
                return False

