import requests
from config_data.config import KEY_API_SCHEDULE
import json
from utils.parsing_website.parser_avia import parser_avia
from utils.parsing_website.parser_train import parser_train
from loader import bot
import os
from utils.global_variables import GlobalVariables
from utils.switch_bool import SwitchBool
from log import logger


def flight_schedules(from_station: str, to_station: str, date: str, name_transport: str, data_message) -> str:
    """Функция поиска маршрутов"""
    logger.log_debug('Запуск функции flight_schedules')
    r = requests.get(
        f'https://api.rasp.yandex.net/v3.0/search/?apikey={KEY_API_SCHEDULE}&format=json&from={from_station}&to={to_station}&'
        f'lang=ru_RU&page=1&date={date}&transport_types={name_transport}')
    if r.status_code == 200:
        json_data = r.json()
        str_result = ''
        result = json_data['segments']
        count_result = len(result)
        if count_result != 0:
            number = 100 // count_result
            count = 0
            if not SwitchBool.high_filt and not SwitchBool.low_filt and not GlobalVariables.custom_filt:
                for i in result:
                    count += number
                    bot.edit_message_text(f'Идёт поиск информации.\nВыполнено: {count}%',
                                          reply_markup=None,
                                          chat_id=data_message.chat.id,
                                          message_id=data_message.message_id + 1)
                    if i["departure"][:10] == date:
                        if not i['tickets_info'] is None and i['tickets_info']['places']:
                            str_result += (f'{i["from"]["title"]}\n'
                                           f'Отправление: {i["departure"][:10]} {i["departure"][11:16]}\n'
                                           f'Часовой пояс: {i["departure"][19:22]}\n'
                                           f'>>>\n'
                                           f'{i["to"]["title"]}\n'
                                           f'Прибытие: {i["arrival"][:10]} {i["arrival"][11:16]}\n'
                                           f'Часовой пояс: {i["arrival"][19:22]}\n\n'
                                           f'Перевозчик - {i["thread"]["carrier"]["title"]}\n'
                                           f'Сайт перевозчика - {i["thread"]["carrier"]["url"]}\n'
                                           f'Цена - {i["tickets_info"]["places"][0]["price"]["whole"]} рублей\n')
                            str_result += '=' * 15 + '\n'
                        else:
                            processed_date_avia = date[8:10] + date[5:7]
                            processed_date_travel = date[8:10] + '.' + date[5:7] + '.' + date[:4]
                            if name_transport == 'plane':
                                with open(os.path.join('utils', 'working_with_the_yandex_api', 'codes_IATA.json'), 'r',
                                          encoding='utf-8') as file_IATA:
                                    dict_IATA = json.load(file_IATA)
                                    if dict_IATA['data'][0].get(i["from"]["title"].upper()) and dict_IATA['data'][0].get(i["to"]["title"].upper()):
                                        result_price_avia = parser_avia(dict_IATA['data'][0][i["from"]["title"].upper()],
                                                    dict_IATA['data'][0][i["to"]["title"].upper()], processed_date_avia,
                                                    i["departure"][11:16], i["arrival"][11:16])
                                        if result_price_avia:
                                            str_result += (f'{i["from"]["title"]}\n'
                                                           f'Отправление: {i["departure"][:10]} {i["departure"][11:16]}\n'
                                                           f'Часовой пояс: {i["departure"][19:22]}\n'
                                                           f'>>>\n'
                                                           f'{i["to"]["title"]}\n'
                                                           f'Прибытие: {i["arrival"][:10]} {i["arrival"][11:16]}\n'
                                                           f'Часовой пояс: {i["arrival"][19:22]}\n\n'
                                                           f'Перевозчик - {i["thread"]["carrier"]["title"]}\n'
                                                           f'Сайт перевозчика - {i["thread"]["carrier"]["url"]}\n'
                                                           f'Цена - {result_price_avia} рублей\n')
                                            str_result += '=' * 15 + '\n'

                                        else:
                                            str_result += (f'{i["from"]["title"]}\n'
                                                           f'Отправление: {i["departure"][:10]} {i["departure"][11:16]}\n'
                                                           f'Часовой пояс: {i["departure"][19:22]}\n'
                                                           f'>>>\n'
                                                           f'{i["to"]["title"]}\n'
                                                           f'Прибытие: {i["arrival"][:10]} {i["arrival"][11:16]}\n'
                                                           f'Часовой пояс: {i["arrival"][19:22]}\n\n'
                                                           f'Перевозчик - {i["thread"]["carrier"]["title"]}\n'
                                                           f'Сайт перевозчика - {i["thread"]["carrier"]["url"]}\n'
                                                           f'Цена - не удалось найти\n')
                                            str_result += '=' * 15 + '\n'
                                    else:
                                        str_result += (f'{i["from"]["title"]}\n'
                                                       f'Отправление: {i["departure"][:10]} {i["departure"][11:16]}\n'
                                                       f'Часовой пояс: {i["departure"][19:22]}\n'
                                                       f'>>>\n'
                                                       f'{i["to"]["title"]}\n'
                                                       f'Прибытие: {i["arrival"][:10]} {i["arrival"][11:16]}\n'
                                                       f'Часовой пояс: {i["arrival"][19:22]}\n\n'
                                                       f'Перевозчик - {i["thread"]["carrier"]["title"]}\n'
                                                       f'Сайт перевозчика - {i["thread"]["carrier"]["url"]}\n'
                                                       f'Цена - не удалось найти\n')
                                        str_result += '=' * 15 + '\n'

                            elif name_transport == 'train':
                                with open(os.path.join('utils', 'working_with_the_yandex_api', 'codes_Rus_RZD.json'), 'r',
                                          encoding='utf-8') as file_RZD:
                                    dict_RZD = json.load(file_RZD)
                                    if dict_RZD['data'][0].get(i["from"]["title"].upper()) and dict_RZD['data'][0].get(i["to"]["title"].upper()):
                                        result_price_train = parser_train(dict_RZD['data'][0][i["from"]["title"].upper()],
                                                    dict_RZD['data'][0][i["to"]["title"].upper()], processed_date_travel,
                                                    i["departure"][11:16], i["arrival"][11:16])
                                        if result_price_train:
                                            str_result += (f'{i["from"]["title"]}\n'
                                                           f'Отправление: {i["departure"][:10]} {i["departure"][11:16]}\n'
                                                           f'Часовой пояс: {i["departure"][19:22]}\n'
                                                           f'>>>\n'
                                                           f'{i["to"]["title"]}\n'
                                                           f'Прибытие: {i["arrival"][:10]} {i["arrival"][11:16]}\n'
                                                           f'Часовой пояс: {i["arrival"][19:22]}\n\n'
                                                           f'Перевозчик - {i["thread"]["carrier"]["title"]}\n'
                                                           f'Сайт перевозчика - {i["thread"]["carrier"]["url"]}\n'
                                                           f'Цена - {result_price_train} рублей\n')
                                            str_result += '=' * 15 + '\n'
                                        else:
                                            str_result += (f'{i["from"]["title"]}\n'
                                                           f'Отправление: {i["departure"][:10]} {i["departure"][11:16]}\n'
                                                           f'Часовой пояс: {i["departure"][19:22]}\n'
                                                           f'>>>\n'
                                                           f'{i["to"]["title"]}\n'
                                                           f'Прибытие: {i["arrival"][:10]} {i["arrival"][11:16]}\n'
                                                           f'Часовой пояс: {i["arrival"][19:22]}\n\n'
                                                           f'Перевозчик - {i["thread"]["carrier"]["title"]}\n'
                                                           f'Сайт перевозчика - {i["thread"]["carrier"]["url"]}\n'
                                                           f'Цена - не удалось найти\n')
                                            str_result += '=' * 15 + '\n'
                                    else:
                                        str_result += (f'{i["from"]["title"]}\n'
                                                       f'Отправление: {i["departure"][:10]} {i["departure"][11:16]}\n'
                                                       f'Часовой пояс: {i["departure"][19:22]}\n'
                                                       f'>>>\n'
                                                       f'{i["to"]["title"]}\n'
                                                       f'Прибытие: {i["arrival"][:10]} {i["arrival"][11:16]}\n'
                                                       f'Часовой пояс: {i["arrival"][19:22]}\n\n'
                                                       f'Перевозчик - {i["thread"]["carrier"]["title"]}\n'
                                                       f'Сайт перевозчика - {i["thread"]["carrier"]["url"]}\n'
                                                       f'Цена - не удалось найти\n')
                                        str_result += '=' * 15 + '\n'
                            else:
                                str_result += (f'{i["from"]["title"]}\n'
                                               f'Отправление: {i["departure"][:10]} {i["departure"][11:16]}\n'
                                               f'Часовой пояс: {i["departure"][19:22]}\n'
                                               f'>>>\n'
                                               f'{i["to"]["title"]}\n'
                                               f'Прибытие: {i["arrival"][:10]} {i["arrival"][11:16]}\n'
                                               f'Часовой пояс: {i["arrival"][19:22]}\n\n'
                                               f'Перевозчик - {i["thread"]["carrier"]["title"]}\n'
                                               f'Сайт перевозчика - {i["thread"]["carrier"]["url"]}\n'
                                               f'Цена - не удалось найти\n')

                                str_result += '=' * 15 + '\n'
                if not count == 100:
                    bot.edit_message_text('Идёт поиск информации.\nВыполнено: 100%',
                                          reply_markup=None,
                                          chat_id=data_message.chat.id,
                                          message_id=data_message.message_id + 1)
                return str_result
            elif SwitchBool.low_filt:
                answer_list = []
                for i in result:
                    count += number
                    bot.edit_message_text(f'Идёт поиск информации.\nВыполнено: {count}%',
                                          reply_markup=None,
                                          chat_id=data_message.chat.id,
                                          message_id=data_message.message_id + 1)
                    if i["departure"][:10] == date:
                        if not i['tickets_info'] is None and i['tickets_info']['places']:
                            answer_list.append([f'{i["from"]["title"]}\n'
                                                f'Отправление: {i["departure"][:10]} {i["departure"][11:16]}\n'
                                                f'Часовой пояс: {i["departure"][19:22]}\n'
                                                f'>>>\n'
                                                f'{i["to"]["title"]}\n'
                                                f'Прибытие: {i["arrival"][:10]} {i["arrival"][11:16]}\n'
                                                f'Часовой пояс: {i["arrival"][19:22]}\n\n'
                                                f'Перевозчик - {i["thread"]["carrier"]["title"]}\n'
                                                f'Сайт перевозчика - {i["thread"]["carrier"]["url"]}\n'
                                                f'Цена - {i["tickets_info"]["places"][0]["price"]["whole"]} рублей\n{"=" * 15}\n',
                                                int(i["tickets_info"]["places"][0]["price"]["whole"])])
                        else:
                            processed_date_avia = date[8:10] + date[5:7]
                            processed_date_travel = date[8:10] + '.' + date[5:7] + '.' + date[:4]
                            if name_transport == 'plane':
                                with open(os.path.join('utils', 'working_with_the_yandex_api', 'codes_IATA.json'), 'r',
                                          encoding='utf-8') as file_IATA:
                                    dict_IATA = json.load(file_IATA)
                                    if dict_IATA['data'][0].get(i["from"]["title"].upper()) and dict_IATA['data'][0].get(
                                            i["to"]["title"].upper()):
                                        result_price_avia = parser_avia(dict_IATA['data'][0][i["from"]["title"].upper()],
                                                                        dict_IATA['data'][0][i["to"]["title"].upper()],
                                                                        processed_date_avia,
                                                                        i["departure"][11:16], i["arrival"][11:16])
                                        if result_price_avia:
                                            answer_list.append([f'{i["from"]["title"]}\n'
                                                                f'Отправление: {i["departure"][:10]} {i["departure"][11:16]}\n'
                                                                f'Часовой пояс: {i["departure"][19:22]}\n'
                                                                f'>>>\n'
                                                                f'{i["to"]["title"]}\n'
                                                                f'Прибытие: {i["arrival"][:10]} {i["arrival"][11:16]}\n'
                                                                f'Часовой пояс: {i["arrival"][19:22]}\n\n'
                                                                f'Перевозчик - {i["thread"]["carrier"]["title"]}\n'
                                                                f'Сайт перевозчика - {i["thread"]["carrier"]["url"]}\n'
                                                                f'Цена - {result_price_avia} рублей\n{"=" * 15}\n',
                                                                int(result_price_avia)])
                            elif name_transport == 'train':
                                with open(os.path.join('utils', 'working_with_the_yandex_api', 'codes_Rus_RZD.json'), 'r',
                                          encoding='utf-8') as file_RZD:
                                    dict_RZD = json.load(file_RZD)
                                    if dict_RZD['data'][0].get(i["from"]["title"].upper()) and dict_RZD['data'][0].get(i["to"]["title"].upper()):
                                        result_price_train = parser_train(dict_RZD['data'][0][i["from"]["title"].upper()],
                                                    dict_RZD['data'][0][i["to"]["title"].upper()], processed_date_travel,
                                                    i["departure"][11:16], i["arrival"][11:16])
                                        if result_price_train:
                                            answer_list.append([f'{i["from"]["title"]}\n'
                                                                f'Отправление: {i["departure"][:10]} {i["departure"][11:16]}\n'
                                                                f'Часовой пояс: {i["departure"][19:22]}\n'
                                                                f'>>>\n'
                                                                f'{i["to"]["title"]}\n'
                                                                f'Прибытие: {i["arrival"][:10]} {i["arrival"][11:16]}\n'
                                                                f'Часовой пояс: {i["arrival"][19:22]}\n\n'
                                                                f'Перевозчик - {i["thread"]["carrier"]["title"]}\n'
                                                                f'Сайт перевозчика - {i["thread"]["carrier"]["url"]}\n'
                                                                f'Цена - {result_price_train} рублей\n{"=" * 15}\n',
                                                                int(result_price_train)])

                if answer_list:
                    minimum = min(answer_list, key=lambda x: x[1])
                    if not count == 100:
                        bot.edit_message_text('Идёт поиск информации.\nВыполнено: 100%',
                                              reply_markup=None,
                                              chat_id=data_message.chat.id,
                                              message_id=data_message.message_id + 1)
                    for l in answer_list:
                        if l[1] == minimum[1]:
                            str_result += l[0]
                    return str_result
                else:
                    return ('Не удалось предоставить минимальную стоимость билета, '
                            'так как во всех результатов поиска, не удалось найти цену на билет.')

            elif SwitchBool.high_filt:
                answer_list = []
                for i in result:
                    count += number
                    bot.edit_message_text(f'Идёт поиск информации.\nВыполнено: {count}%',
                                          reply_markup=None,
                                          chat_id=data_message.chat.id,
                                          message_id=data_message.message_id + 1)
                    if i["departure"][:10] == date:
                        if not i['tickets_info'] is None and i['tickets_info']['places']:
                            answer_list.append([f'{i["from"]["title"]}\n'
                                                f'Отправление: {i["departure"][:10]} {i["departure"][11:16]}\n'
                                                f'Часовой пояс: {i["departure"][19:22]}\n'
                                                f'>>>\n'
                                                f'{i["to"]["title"]}\n'
                                                f'Прибытие: {i["arrival"][:10]} {i["arrival"][11:16]}\n'
                                                f'Часовой пояс: {i["arrival"][19:22]}\n\n'
                                                f'Перевозчик - {i["thread"]["carrier"]["title"]}\n'
                                                f'Сайт перевозчика - {i["thread"]["carrier"]["url"]}\n'
                                                f'Цена - {i["tickets_info"]["places"][0]["price"]["whole"]} рублей\n{"=" * 15}\n',
                                                int(i["tickets_info"]["places"][0]["price"]["whole"])])
                        else:
                            processed_date_avia = date[8:10] + date[5:7]
                            processed_date_travel = date[8:10] + '.' + date[5:7] + '.' + date[:4]
                            if name_transport == 'plane':
                                with open(os.path.join('utils', 'working_with_the_yandex_api', 'codes_IATA.json'), 'r',
                                          encoding='utf-8') as file_IATA:
                                    dict_IATA = json.load(file_IATA)
                                    if dict_IATA['data'][0].get(i["from"]["title"].upper()) and dict_IATA['data'][0].get(
                                            i["to"]["title"].upper()):
                                        result_price_avia = parser_avia(dict_IATA['data'][0][i["from"]["title"].upper()],
                                                                        dict_IATA['data'][0][i["to"]["title"].upper()],
                                                                        processed_date_avia,
                                                                        i["departure"][11:16], i["arrival"][11:16])
                                        if result_price_avia:
                                            answer_list.append([f'{i["from"]["title"]}\n'
                                                                f'Отправление: {i["departure"][:10]} {i["departure"][11:16]}\n'
                                                                f'Часовой пояс: {i["departure"][19:22]}\n'
                                                                f'>>>\n'
                                                                f'{i["to"]["title"]}\n'
                                                                f'Прибытие: {i["arrival"][:10]} {i["arrival"][11:16]}\n'
                                                                f'Часовой пояс: {i["arrival"][19:22]}\n\n'
                                                                f'Перевозчик - {i["thread"]["carrier"]["title"]}\n'
                                                                f'Сайт перевозчика - {i["thread"]["carrier"]["url"]}\n'
                                                                f'Цена - {result_price_avia} рублей\n{"=" * 15}\n',
                                                                int(result_price_avia)])
                            elif name_transport == 'train':
                                with open(os.path.join('utils', 'working_with_the_yandex_api', 'codes_Rus_RZD.json'), 'r',
                                          encoding='utf-8') as file_RZD:
                                    dict_RZD = json.load(file_RZD)
                                    if dict_RZD['data'][0].get(i["from"]["title"].upper()) and dict_RZD['data'][0].get(
                                            i["to"]["title"].upper()):
                                        result_price_train = parser_train(dict_RZD['data'][0][i["from"]["title"].upper()],
                                                                           dict_RZD['data'][0][i["to"]["title"].upper()],
                                                                           processed_date_travel,
                                                                           i["departure"][11:16], i["arrival"][11:16])
                                        if result_price_train:
                                            answer_list.append([f'{i["from"]["title"]}\n'
                                                                f'Отправление: {i["departure"][:10]} {i["departure"][11:16]}\n'
                                                                f'Часовой пояс: {i["departure"][19:22]}\n'
                                                                f'>>>\n'
                                                                f'{i["to"]["title"]}\n'
                                                                f'Прибытие: {i["arrival"][:10]} {i["arrival"][11:16]}\n'
                                                                f'Часовой пояс: {i["arrival"][19:22]}\n\n'
                                                                f'Перевозчик - {i["thread"]["carrier"]["title"]}\n'
                                                                f'Сайт перевозчика - {i["thread"]["carrier"]["url"]}\n'
                                                                f'Цена - {result_price_train} рублей\n{"=" * 15}\n',
                                                                int(result_price_train)])
                if answer_list:
                    maximum = max(answer_list, key=lambda x: x[1])
                    if not count == 100:
                        bot.edit_message_text('Идёт поиск информации.\nВыполнено: 100%',
                                              reply_markup=None,
                                              chat_id=data_message.chat.id,
                                              message_id=data_message.message_id + 1)
                    for l in answer_list:
                        if l[1] == maximum[1]:
                            str_result += l[0]
                    return str_result
                else:
                    return ('Не удалось предоставить максимальную стоимость билета, '
                            'так как во всех результатов поиска, не удалось найти цену на билет.')
            else:
                for i in result:
                    count += number
                    bot.edit_message_text(f'Идёт поиск информации.\nВыполнено: {count}%',
                                          reply_markup=None,
                                          chat_id=data_message.chat.id,
                                          message_id=data_message.message_id + 1)
                    if i["departure"][:10] == date:
                        if not i['tickets_info'] is None and i['tickets_info']['places']:
                            if GlobalVariables.custom_filt[0] <= int(i['tickets_info']['places'][0]["price"]["whole"]) and GlobalVariables.custom_filt[1] >= int(i['tickets_info']['places'][0]["price"]["whole"]):
                                str_result += (f'{i["from"]["title"]}\n'
                                               f'Отправление: {i["departure"][:10]} {i["departure"][11:16]}\n'
                                               f'Часовой пояс: {i["departure"][19:22]}\n'
                                               f'>>>\n'
                                               f'{i["to"]["title"]}\n'
                                               f'Прибытие: {i["arrival"][:10]} {i["arrival"][11:16]}\n'
                                               f'Часовой пояс: {i["arrival"][19:22]}\n\n'
                                               f'Перевозчик - {i["thread"]["carrier"]["title"]}\n'
                                               f'Сайт перевозчика - {i["thread"]["carrier"]["url"]}\n'
                                               f'Цена - {i["tickets_info"]["places"][0]["price"]["whole"]} рублей\n')
                                str_result += '=' * 15 + '\n'
                        else:
                            processed_date_avia = date[8:10] + date[5:7]
                            processed_date_travel = date[8:10] + '.' + date[5:7] + '.' + date[:4]
                            if name_transport == 'plane':
                                with open(os.path.join('utils', 'working_with_the_yandex_api', 'codes_IATA.json'), 'r',
                                          encoding='utf-8') as file_IATA:
                                    dict_IATA = json.load(file_IATA)
                                    if dict_IATA['data'][0].get(i["from"]["title"].upper()) and dict_IATA['data'][0].get(
                                            i["to"]["title"].upper()):
                                        result_price_avia = parser_avia(dict_IATA['data'][0][i["from"]["title"].upper()],
                                                                        dict_IATA['data'][0][i["to"]["title"].upper()],
                                                                        processed_date_avia,
                                                                        i["departure"][11:16], i["arrival"][11:16])
                                        if result_price_avia:
                                            if GlobalVariables.custom_filt[0] <= int(result_price_avia) and GlobalVariables.custom_filt[1] >= int(result_price_avia):
                                                str_result += (f'{i["from"]["title"]}\n'
                                                               f'Отправление: {i["departure"][:10]} {i["departure"][11:16]}\n'
                                                               f'Часовой пояс: {i["departure"][19:22]}\n'
                                                               f'>>>\n'
                                                               f'{i["to"]["title"]}\n'
                                                               f'Прибытие: {i["arrival"][:10]} {i["arrival"][11:16]}\n'
                                                               f'Часовой пояс: {i["arrival"][19:22]}\n\n'
                                                               f'Перевозчик - {i["thread"]["carrier"]["title"]}\n'
                                                               f'Сайт перевозчика - {i["thread"]["carrier"]["url"]}\n'
                                                               f'Цена - {result_price_avia} рублей\n')
                                                str_result += '=' * 15 + '\n'
                            elif name_transport == 'train':
                                with open(os.path.join('utils', 'working_with_the_yandex_api', 'codes_Rus_RZD.json'), 'r',
                                          encoding='utf-8') as file_RZD:
                                    dict_RZD = json.load(file_RZD)
                                    if dict_RZD['data'][0].get(i["from"]["title"].upper()) and dict_RZD['data'][0].get(
                                            i["to"]["title"].upper()):
                                        result_price_train = parser_train(dict_RZD['data'][0][i["from"]["title"].upper()],
                                                                           dict_RZD['data'][0][i["to"]["title"].upper()],
                                                                           processed_date_travel,
                                                                           i["departure"][11:16], i["arrival"][11:16])
                                        if result_price_train:
                                            if GlobalVariables.custom_filt[0] <= int(result_price_train) and GlobalVariables.custom_filt[1] >= int(result_price_train):
                                                str_result += (f'{i["from"]["title"]}\n'
                                                               f'Отправление: {i["departure"][:10]} {i["departure"][11:16]}\n'
                                                               f'Часовой пояс: {i["departure"][19:22]}\n'
                                                               f'>>>\n'
                                                               f'{i["to"]["title"]}\n'
                                                               f'Прибытие: {i["arrival"][:10]} {i["arrival"][11:16]}\n'
                                                               f'Часовой пояс: {i["arrival"][19:22]}\n\n'
                                                               f'Перевозчик - {i["thread"]["carrier"]["title"]}\n'
                                                               f'Сайт перевозчика - {i["thread"]["carrier"]["url"]}\n'
                                                               f'Цена - {result_price_train} рублей\n')
                                                str_result += '=' * 15 + '\n'
                if str_result:
                    if not count == 100:
                        bot.edit_message_text('Идёт поиск информации.\nВыполнено: 100%',
                                              reply_markup=None,
                                              chat_id=data_message.chat.id,
                                              message_id=data_message.message_id + 1)
                        return str_result
                else:
                    return ('Не удалось предоставить стоимость билета в указанном диапазоне,'
                            'так как во всех результатов поиска, не удалось найти цену на билет, '
                            'либо цена не входит в заданный диапазон.')
        else:
            return ('К сожалению поиск по вашим параметрам не дал результатов.\n'
                    'Попробуйте поменять ваши параметры, возможно это повлияет на конечный результат.')
    else:
        return ('К сожалению поиск по вашим параметрам не дал результатов.\n'
                'Попробуйте поменять ваши параметры, возможно это повлияет на конечный результат.')
