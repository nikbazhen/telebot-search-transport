from utils.working_with_the_yandex_api.check_codes_yandex import check_codes_yandex
from states.route_info import RouteInfo
from loader import bot
from database.data import User, History
from database.check_registration_db import check
from telebot.types import ReplyKeyboardRemove
from keyboards.reply.transport_button import transport_markup
from utils.working_with_the_yandex_api.nearest_stations import search_nearest_stations
from log import logger
from telegram_bot_calendar import LSTEP, DetailedTelegramCalendar
from utils.check_date import check_date
from utils.working_with_the_yandex_api.flight_schedules_between_stations import flight_schedules
from utils.switch_bool import SwitchBool
from utils.global_variables import GlobalVariables
import datetime
import timezonefinder
import pytz
import math
from utils.decarated_errors import decorator_error


@bot.message_handler(commands=['route_search'])
@decorator_error
def route_search(message):
    """Функция обработки команды /route_search"""
    logger.log_debug('Запуск функции route_search')
    GlobalVariables.id_chat_for_errors = message.chat.id
    if check(message.chat.id):
        bot.set_state(message.chat.id, RouteInfo.transport, message.chat.id)
        bot.send_message(message.chat.id, 'Выберите транспорт отправления, нажав соответствующую кнопку:',
                         reply_markup=transport_markup())
    else:
        bot.send_message(message.chat.id, 'Для использования этой команды необходимо пройти регистрацию!')


@bot.message_handler(state=RouteInfo.transport)
@decorator_error
def transport_user(message):
    """Функция обработки состояния RouteInfo.transport"""
    logger.log_debug('Запуск функции transport_user')
    from keyboards.inline.starting_and_stop_point_button import starting_and_stop_point_button
    if message.text == 'Самолёт':
        bot.set_state(message.chat.id, RouteInfo.starting_point, message.chat.id)
        with bot.retrieve_data(message.chat.id, message.chat.id) as data:
            data['transport'] = 'plane'
            GlobalVariables.answer_transport = 'plane'
            GlobalVariables.transport_for_db = 'Транспорт - самолёт'
            bot.send_message(message.chat.id, 'Вы выбрали самолёт.', reply_markup=ReplyKeyboardRemove())
            lng = User.select(User.longitude_adress).where(User.id_user == message.from_user.id)[0].longitude_adress
            lat = User.select(User.latitude_adress).where(User.id_user == message.from_user.id)[0].latitude_adress
            GlobalVariables.latitude = float(lat)
            GlobalVariables.longitude = float(lng)
            GlobalVariables.stations = search_nearest_stations(lng, lat, data['transport'])
            if GlobalVariables.stations:
                bot.send_message(message.chat.id, 'Введите или выберите начальную точку отправления.')

                bot.send_message(message.chat.id,
                                 'Доступные варианты в радиусе 100 километров, от вашего населённого пункта:',
                                 reply_markup=starting_and_stop_point_button(GlobalVariables.stations, 'start'))
            else:
                bot.send_message(message.chat.id, 'В радиусе 100 километров, от вашего населённого пункта,'
                                                  ' не найдена хотя бы одна остановочная платформа, '
                                                  'по вашему выбранному транспорту.\n'
                                                  'Попробуйте ввести начальную точку отправления в ручную.',
                                 reply_markup=ReplyKeyboardRemove())

    elif message.text == 'Поезд':
        bot.set_state(message.chat.id, RouteInfo.starting_point, message.chat.id)
        with bot.retrieve_data(message.chat.id, message.chat.id) as data:
            data['transport'] = 'train'
            GlobalVariables.answer_transport = 'train'
            GlobalVariables.transport_for_db = 'Транспорт - поезд'
            bot.send_message(message.chat.id, 'Вы выбрали поезд.', reply_markup=ReplyKeyboardRemove())
            lng = User.select(User.longitude_adress).where(User.id_user == message.from_user.id)[0].longitude_adress
            lat = User.select(User.latitude_adress).where(User.id_user == message.from_user.id)[0].latitude_adress
            GlobalVariables.latitude = float(lat)
            GlobalVariables.longitude = float(lng)
            GlobalVariables.stations = search_nearest_stations(lng, lat, data['transport'])
            if GlobalVariables.stations:
                bot.send_message(message.chat.id, 'Введите или выберите начальную точку отправления.')
                bot.send_message(message.chat.id,
                                 'Доступные варианты в радиусе 100 километров, от вашего населённого пункта:',
                                 reply_markup=starting_and_stop_point_button(GlobalVariables.stations, 'start'))
            else:
                bot.send_message(message.chat.id, 'В радиусе 100 километров, от вашего населённого пункта,'
                                                  ' не найдена хотя бы одна остановочная платформа, '
                                                  'по вашему выбранному транспорту.\n'
                                                  'Попробуйте ввести начальную точку отправления в ручную.',
                                 reply_markup=ReplyKeyboardRemove())
    elif message.text == 'Электричка':
        bot.set_state(message.chat.id, RouteInfo.starting_point, message.chat.id)
        with bot.retrieve_data(message.chat.id, message.chat.id) as data:
            data['transport'] = 'suburban'
            GlobalVariables.answer_transport = 'suburban'
            GlobalVariables.transport_for_db = 'Транспорт - электричка'
            bot.send_message(message.chat.id, 'Вы выбрали электричку.', reply_markup=ReplyKeyboardRemove())
            lng = User.select(User.longitude_adress).where(User.id_user == message.from_user.id)[0].longitude_adress
            lat = User.select(User.latitude_adress).where(User.id_user == message.from_user.id)[0].latitude_adress
            GlobalVariables.latitude = float(lat)
            GlobalVariables.longitude = float(lng)
            GlobalVariables.stations = search_nearest_stations(lng, lat, data['transport'])
            if GlobalVariables.stations:
                bot.send_message(message.chat.id, 'Введите (можно указать название населённого пункта) или'
                                                  ' выберите начальную точку отправления.')
                bot.send_message(message.chat.id,
                                 'Доступные варианты в радиусе 100 километров, от вашего населённого пункта:',
                                 reply_markup=starting_and_stop_point_button(GlobalVariables.stations, 'start'))
            else:
                bot.send_message(message.chat.id, 'В радиусе 100 километров, от вашего населённого пункта,'
                                                  ' не найдена хотя бы одна остановочная платформа,'
                                                  ' по вашему выбранному транспорту.\n'
                                                  'Попробуйте ввести начальную точку отправления в ручную.',
                                 reply_markup=ReplyKeyboardRemove())
    elif message.text == 'Автобус':
        bot.set_state(message.chat.id, RouteInfo.starting_point, message.chat.id)
        with bot.retrieve_data(message.chat.id, message.chat.id) as data:
            data['transport'] = 'bus'
            GlobalVariables.answer_transport = 'bus'
            GlobalVariables.transport_for_db = 'Транспорт - автобус'
            bot.send_message(message.chat.id, 'Вы выбрали автобус.', reply_markup=ReplyKeyboardRemove())
            lng = User.select(User.longitude_adress).where(User.id_user == message.from_user.id)[0].longitude_adress
            lat = User.select(User.latitude_adress).where(User.id_user == message.from_user.id)[0].latitude_adress
            GlobalVariables.latitude = float(lat)
            GlobalVariables.longitude = float(lng)
            GlobalVariables.stations = search_nearest_stations(lng, lat, data['transport'])
            if GlobalVariables.stations:
                bot.send_message(message.chat.id, 'Введите (можно указать название населённого пункта) или '
                                                  'выберите начальную точку отправления.')
                bot.send_message(message.chat.id,
                                 'Доступные варианты в радиусе 100 километров, от вашего населённого пункта:',
                                 reply_markup=starting_and_stop_point_button(GlobalVariables.stations, 'start'))
            else:
                bot.send_message(message.chat.id, 'В радиусе 100 километров, от вашего населённого пункта,'
                                                  ' не найдена хотя бы одна остановочная платформа, '
                                                  'по вашему выбранному транспорту.\n'
                                                  'Попробуйте ввести начальную точку отправления в ручную.',
                                 reply_markup=ReplyKeyboardRemove())

    else:
        bot.send_message(message.chat.id, 'Выберите транспорт отправления, нажав соответствующую кнопку:',
                         reply_markup=transport_markup())


@bot.message_handler(state=RouteInfo.starting_point)
@decorator_error
def starting_point(message, answer=None, check_button=False):
    """Функция обработки состояния RouteInfo.starting_point"""
    logger.log_debug('Запуск функции starting_point')
    if not check_button:
        if not SwitchBool.checking_button_removal_start_point:
            SwitchBool.checking_button_removal_start_point = True
            bot.edit_message_reply_markup(message.chat.id, message_id=message.message_id - 1, reply_markup='')
        cod_station = check_codes_yandex(message.text, GlobalVariables.answer_transport)
        if isinstance(cod_station, list) and cod_station[0] is None:
            bot.send_message(message.chat.id, f'Найдено два совпадения:\n - {cod_station[1]}\n - {cod_station[2]}\n'
                                              f'Введите один из предложенных вариантов, который вам нужен, '
                                              f'в точности так же, как и написано.\n'
                                              f'Например, если вам нужен населённый пункт, '
                                              f'то нужно ввести: {cod_station[2]}.')
        elif cod_station:
            SwitchBool.checking_button_removal_start_point = False
            bot.set_state(message.chat.id, RouteInfo.stop_point, message.chat.id)
            with bot.retrieve_data(message.chat.id, message.chat.id) as data:
                data['starting_point'] = cod_station
                GlobalVariables.start_for_db = 'Начальная точка - ' + message.text.title()
                if GlobalVariables.stations and data['transport'] != 'plane' and data['transport'] != 'train':
                    from keyboards.inline.starting_and_stop_point_button import starting_and_stop_point_button
                    bot.send_message(message.chat.id, 'Введите (можно указать название населённого пункта) или'
                                                      ' выберите конечную точку отправления.')
                    bot.send_message(message.chat.id,
                                     'Доступные варианты в радиусе 100 километров, от вашего населённого пункта:',
                                     reply_markup=starting_and_stop_point_button(GlobalVariables.stations, 'stop'))
                else:
                    bot.send_message(message.chat.id, 'Введите конечную точку отправления или названия населённого')
                    SwitchBool.checking_button_removal_stop_point = True
        else:
            bot.send_message(message.chat.id, 'Не найдена остановочная платформа.\n'
                                              'Убедитесь что остановочная платформа введена '
                                              'корректно и повторите попытку')
    elif check_button:
        bot.set_state(message.chat.id, RouteInfo.stop_point, message.chat.id)
        with bot.retrieve_data(message.chat.id, message.chat.id) as data:
            data['starting_point'] = answer[0]
            GlobalVariables.start_for_db = 'Начальная точка - ' + answer[1].title()
            if GlobalVariables.stations and data['transport'] != 'plane' and data['transport'] != 'train':
                from keyboards.inline.starting_and_stop_point_button import starting_and_stop_point_button
                bot.send_message(message.chat.id, 'Введите (можно указать название населённого пункта) или '
                                                  'выберите конечную точку отправления.')
                bot.send_message(message.chat.id,
                                 'Доступные варианты в радиусе 100 километров, от вашего населённого пункта:',
                                 reply_markup=starting_and_stop_point_button(GlobalVariables.stations, 'stop'))
            else:
                bot.send_message(message.chat.id, 'Введите конечную точку отправления или '
                                                  'названия населённого пункта')
                SwitchBool.checking_button_removal_stop_point = True


@bot.message_handler(state=RouteInfo.stop_point)
@decorator_error
def stop_point(message, answer=None, check_button=False):
    """Функция обработки состояния RouteInfo.stop_point"""
    logger.log_debug('Запуск функции stop_point')
    from keyboards.inline import calendar_button
    if not check_button:
        if not SwitchBool.checking_button_removal_stop_point:
            SwitchBool.checking_button_removal_stop_point = True
            bot.edit_message_reply_markup(message.chat.id, message_id=message.message_id - 1, reply_markup='')
        cod_station = check_codes_yandex(message.text, GlobalVariables.answer_transport)
        if isinstance(cod_station, list) and cod_station[0] is None:
            bot.send_message(message.chat.id, f'Найдено два совпадения:\n - {cod_station[1]}\n - {cod_station[2]}\n'
                                              f'Введите один из предложенных вариантов, который вам нужен, '
                                              f'в точности так же, как и написано.\n'
                                              f'Например, если вам нужен населённый пункт, '
                                              f'то нужно ввести: {cod_station[2]}.')

        elif cod_station:
            SwitchBool.checking_button_removal_stop_point = False
            bot.set_state(message.chat.id, RouteInfo.date, message.chat.id)
            with bot.retrieve_data(message.chat.id, message.chat.id) as data:
                data['stop_point'] = cod_station
                GlobalVariables.stop_for_db = 'Конечная точка - ' + message.text.title()
                SwitchBool.checking_button_removal_stop_point = False
                calendar, step = DetailedTelegramCalendar(locale='ru').build()
                bot.send_message(message.chat.id, f'Выберите дату или введите её в ручную в формате "YYYY-MM-DD"'
                                                  f'(Год.Месяц.Число.Например: 2000-01-01)\n'
                                                  f'Выберите {LSTEP[step][0]}:',
                                 reply_markup=calendar)

        else:
            bot.send_message(message.chat.id, 'Не найдена остановочная платформа.\n'
                                              'Убедитесь что остановочная платформа введена '
                                              'корректно и повторите попытку')
    elif check_button:
        bot.set_state(message.chat.id, RouteInfo.date, message.chat.id)
        with bot.retrieve_data(message.chat.id, message.chat.id) as data:
            data['stop_point'] = answer[0]
            GlobalVariables.stop_for_db = 'Конечная точка - ' + answer[1].title()
            calendar, step = DetailedTelegramCalendar(locale='ru').build()
            bot.send_message(message.chat.id, f'Выберите дату или введите её в ручную в формате "YYYY-MM-DD" '
                                              f'(Год-Месяц-Число.) Например: 2000-01-01.\n'
                                              f'Выберите {LSTEP[step][0]}:', reply_markup=calendar)


@bot.message_handler(state=RouteInfo.date)
@decorator_error
def departure_date(message, answer=None, check_button=False):
    """Функция обработки состояния RouteInfo.date"""
    logger.log_debug('Запуск функции departure_date')
    if not check_button:
        bot.edit_message_reply_markup(message.chat.id, message_id=message.message_id - 1, reply_markup='')
        if check_date(message.text, GlobalVariables.latitude, GlobalVariables.longitude):
            bot.set_state(message.chat.id, RouteInfo.stop_func, message.chat.id)
            with bot.retrieve_data(message.chat.id, message.chat.id) as data:
                data['date'] = message.text
                GlobalVariables.date_for_db = 'Выбранная дата - ' + message.text
                bot.send_message(message.chat.id, 'Идёт поиск информации.\nВыполнено: 0%')
                final_answer = flight_schedules(data['starting_point'], data['stop_point'],
                                                data['date'], data['transport'], message)
                if len(final_answer) > 4096:
                    count = int(math.ceil(len(final_answer) / 4096))
                    for x in range(1, count):
                        if count != x:
                            bot.send_message(message.chat.id, final_answer[0 + (4096 * x - 4096):4096 * x + 1],
                                             disable_web_page_preview=True)
                        else:
                            bot.send_message(message.chat.id, final_answer[4096 * (x - 1):],
                                             disable_web_page_preview=True)
                if final_answer == (
                'Не удалось предоставить стоимость билета в указанном диапазоне, так как во всех результатов поиска, не удалось найти цену на билет.'
                ) or final_answer == (
                'К сожалению поиск по вашим параметрам не дал результатов.\nПопробуйте поменять ваши параметры, возможно это повлияет на конечный результат.'
                ) or final_answer == (
                'Не удалось предоставить максимальную стоимость билета, так как во всех результатов поиска, не удалось найти цену на билет.'
                ) or final_answer == (
                'Не удалось предоставить минимальную стоимость билета, так как во всех результатов поиска, не удалось найти цену на билет.'):
                    GlobalVariables.resul_for_db = 'Результат - поиск не дал результата.'
                else:
                    GlobalVariables.resul_for_db = 'Результат - поиск дал результат.'
                if GlobalVariables.custom_filt:
                    GlobalVariables.search_parameter_for_db = 'Параметр поиска - поиск в заданном диапазоне цены.'
                elif SwitchBool.low_filt:
                    GlobalVariables.search_parameter_for_db = 'Параметр поиска - поиск самого дешёвого билета.'
                elif SwitchBool.high_filt:
                    GlobalVariables.search_parameter_for_db = 'Параметр поиска - поиск самого дорогого билета.'
                else:
                    GlobalVariables.search_parameter_for_db = 'Параметр поиска - общий поиск.'

                tf = timezonefinder.TimezoneFinder()
                timezone_str = tf.certain_timezone_at(lat=GlobalVariables.latitude,
                                                      lng=GlobalVariables.latitude)
                timezone = pytz.timezone(timezone_str)
                dt = datetime.datetime.utcnow()
                GlobalVariables.date_search_for_db = 'Дата поиска - ' + str(dt + timezone.utcoffset(dt))[:-7]

                records = History.select().where(History.id_user == message.chat.id)
                if len(records) == 10:
                    record = records[0].date_search
                    History.delete().where(History.date_search == record).execute()

                create_history_db = History(
                    id_user=message.chat.id,
                    start=GlobalVariables.start_for_db,
                    stop=GlobalVariables.stop_for_db,
                    date=GlobalVariables.date_for_db,
                    transport=GlobalVariables.transport_for_db,
                    result=GlobalVariables.resul_for_db,
                    search_parameter=GlobalVariables.search_parameter_for_db,
                    date_search=GlobalVariables.date_search_for_db)
                create_history_db.save(force_insert=True)

                SwitchBool.high_filt = False
                SwitchBool.low_filt = False
                GlobalVariables.custom_filt = None
                GlobalVariables.date_search_for_db = None
                GlobalVariables.search_parameter_for_db = None
                GlobalVariables.resul_for_db = None
                GlobalVariables.transport_for_db = None
                GlobalVariables.date_for_db = None
                GlobalVariables.stop_for_db = None
                GlobalVariables.start_for_db = None

        else:
            from keyboards.inline import calendar_button
            calendar, step = DetailedTelegramCalendar(locale='ru').build()
            bot.send_message(message.chat.id, f'Введённая дата уже прошла, либо введена не верно.\n'
                                              f'Если вы вводите дату вручную, формат должен '
                                              f'соответствовать "YYYY-MM-DD" '
                                              f'(Год.Месяц.Число.) Например: 2000-01-01\n'
                                              f'Выберите {LSTEP[step][0]}:', reply_markup=calendar)
    elif check_button:
        if check_date(answer, GlobalVariables.latitude, GlobalVariables.longitude):
            bot.set_state(message.chat.id, RouteInfo.stop_func, message.chat.id)
            with bot.retrieve_data(message.chat.id, message.chat.id) as data:
                data['date'] = answer
                GlobalVariables.date_for_db = 'Выбранная дата - ' + answer
                bot.send_message(message.chat.id, 'Идёт поиск информации.\nВыполнено: 0%')
                final_answer = flight_schedules(data['starting_point'], data['stop_point'],
                                                data['date'], data['transport'], message)
                if len(final_answer) > 4095:
                    count = int(math.ceil(len(final_answer) / 4095))
                    for x in range(1, count + 1):
                        if count != x:
                            bot.send_message(message.chat.id, final_answer[0 + (4095 * x - 4095):4095 * x + 1],
                                             disable_web_page_preview=True)
                        else:
                            bot.send_message(message.chat.id, final_answer[4096 * (x - 1):],
                                             disable_web_page_preview=True)
                else:
                    bot.send_message(message.chat.id, final_answer, disable_web_page_preview=True)
                if final_answer == ('Не удалось предоставить стоимость билета в указанном диапазоне,'
                            'так как во всех результатов поиска, не удалось найти цену на билет, '
                            'либо цена не входит в заданный диапазон.') or final_answer == (
                'К сожалению поиск по вашим параметрам не дал результатов.\nПопробуйте поменять ваши параметры, возможно это повлияет на конечный результат.'
                ) or final_answer == (
                'Не удалось предоставить максимальную стоимость билета, так как во всех результатов поиска, не удалось найти цену на билет.'
                ) or final_answer == (
                'Не удалось предоставить стоимость билета в указанном диапазоне,'
                        'так как во всех результатов поиска, не удалось найти цену на билет.'):
                    GlobalVariables.resul_for_db = 'Результат - поиск не дал результата.'
                else:
                    GlobalVariables.resul_for_db = 'Результат - поиск дал результат.'
                if GlobalVariables.custom_filt:
                    GlobalVariables.search_parameter_for_db = 'Параметр поиска - поиск в заданном диапазоне цены.'
                elif SwitchBool.low_filt:
                    GlobalVariables.search_parameter_for_db = 'Параметр поиска - поиск самого дешёвого билета.'
                elif SwitchBool.high_filt:
                    GlobalVariables.search_parameter_for_db = 'Параметр поиска - поиск самого дорогого билета.'
                else:
                    GlobalVariables.search_parameter_for_db = 'Параметр поиска - общий поиск.'

                tf = timezonefinder.TimezoneFinder()
                timezone_str = tf.certain_timezone_at(lat=GlobalVariables.latitude,
                                                      lng=GlobalVariables.longitude)
                timezone = pytz.timezone(timezone_str)
                dt = datetime.datetime.utcnow()
                GlobalVariables.date_search_for_db = 'Дата поиска - ' + str(dt + timezone.utcoffset(dt))[:-7]

                records = History.select().where(History.id_user == message.chat.id)
                if len(records) == 10:
                    record = records[0].date_search
                    History.delete().where(History.date_search == record).execute()

                create_history_db = History(
                    id_user=message.chat.id,
                    start=GlobalVariables.start_for_db,
                    stop=GlobalVariables.stop_for_db,
                    date=GlobalVariables.date_for_db,
                    transport=GlobalVariables.transport_for_db,
                    result=GlobalVariables.resul_for_db,
                    search_parameter=GlobalVariables.search_parameter_for_db,
                    date_search=GlobalVariables.date_search_for_db)
                create_history_db.save(force_insert=True)

                SwitchBool.high_filt = False
                SwitchBool.low_filt = False
                GlobalVariables.custom_filt = None
                GlobalVariables.date_search_for_db = None
                GlobalVariables.search_parameter_for_db = None
                GlobalVariables.resul_for_db = None
                GlobalVariables.transport_for_db = None
                GlobalVariables.date_for_db = None
                GlobalVariables.stop_for_db = None
                GlobalVariables.start_for_db = None

        else:
            from keyboards.inline import calendar_button
            calendar, step = DetailedTelegramCalendar(locale='ru').build()
            bot.send_message(message.chat.id, f'Выбранная дата уже прошла.\n'
                                              f'Повторите выбор или введите дату в ручную, '
                                              f'в формате "YYYY-MM-DD" '
                                              f'(Год-Месяц-Число.) Например: 2000-01-01\n'
                                              f'Выберите {LSTEP[step][0]}:',
                             reply_markup=calendar)

    @bot.message_handler(state=RouteInfo.stop_func)
    def pass_func():
        """
        Функция для выхода из состояния (сторонняя библиотека 'calendar-telebot',
         зацикливает действующие состояние (функция delete_state, положительного результата не даёт))
        """
        pass
