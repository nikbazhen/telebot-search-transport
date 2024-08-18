from states.user_info_change import UserInfoChange
from utils.working_with_the_yandex_api.address_from_coords import get_address
from loader import bot
from database.data import User
from database.check_registration_db import check
from telebot.types import ReplyKeyboardRemove
from keyboards.reply.request_location import request_location
from log import logger
from utils.decarated_errors import decorator_error


@bot.message_handler(commands=['changing_credentials'])
@decorator_error
def registration1(message):
    """Функция обработки команды /changing_credentials"""
    logger.log_debug('Запуск функции registration1')
    if check(message.chat.id):
        User.delete().where(User.id_user == message.chat.id).execute()
        bot.set_state(message.chat.id, UserInfoChange.name, message.chat.id)
        bot.send_message(message.chat.id, 'Введите ваше имя',  reply_markup=ReplyKeyboardRemove())
    else:
        bot.send_message(message.chat.id, f'Вы ещё не зарегистрировались, что бы менять данные!',
                         reply_markup=ReplyKeyboardRemove())


@bot.message_handler(state=UserInfoChange.name)
@decorator_error
def get_name1(message):
    """Функция обработки состояния UserInfoChange.name"""
    logger.log_debug('Запуск функции get_name1')
    if message.text.isalpha():
        bot.set_state(message.chat.id, UserInfoChange.polity_city, message.chat.id)
        bot.send_message(message.chat.id, 'Чтобы определить ваше местоположение, нажмите на кнопку'
                                          ' "Поделиться местоположением" или '
                                          'напишите ваше текущее местоположение, если вы пользуетесь Telegram '
                                          'с помощью ПК',
                         reply_markup=request_location())
        with bot.retrieve_data(message.chat.id, message.chat.id) as data:
            data['name'] = message.text

    else:
        bot.send_message(message.chat.id, 'Имя должно состоять только из букв.\n'
                                          'Повторите ввод.')


@bot.message_handler(content_types=['location', 'text'], state=UserInfoChange.polity_city)
@decorator_error
def get_polity_city1(message):
    """Функция обработки состояния UserInfoChange.polity_city"""
    logger.log_debug('Запуск функции get_polity_city1')
    if message.content_type == 'location':
        longitude = str(message.location.longitude)
        latitude = str(message.location.latitude)
        geo = get_address(longitude, latitude)
        with bot.retrieve_data(message.chat.id, message.chat.id) as data:
            data['polity_city'] = geo
            bot.send_message(message.chat.id, 'Перезапись данных прошла успешно!', reply_markup=ReplyKeyboardRemove())
            bot.send_message(message.chat.id, f'Вот ваши данные:\n'
                                              f'Имя - {data["name"]}\n'
                                              f'Местоположение - {data["polity_city"]},\n')
            create_user_db = User(id_user=message.chat.id, name=data['name'], polity_city=data['polity_city'],
                                 latitude_adress=latitude, longitude_adress=longitude)
            create_user_db.save(force_insert=True)
        bot.delete_state(message.from_user.id, message.chat.id)
    elif message.content_type == 'text':
        geo = get_address(message.text)
        if not geo[0]:
            bot.send_message(message.chat.id, geo[1], reply_markup=request_location())
        else:
            with bot.retrieve_data(message.chat.id, message.chat.id) as data:
                data['polity_city'] = geo[0]
                bot.send_message(message.chat.id, 'Перезапись данных прошла успешно!', reply_markup=ReplyKeyboardRemove())
                bot.send_message(message.chat.id, f'Вот ваши данные:\n'
                                                  f'Имя - {data["name"]}\n'
                                                  f'Местоположение - {data["polity_city"]},\n')
                create_user_db = User(id_user=message.chat.id, name=data['name'], polity_city=data['polity_city'],
                                      latitude_adress=geo[1][1], longitude_adress=geo[1][0])
                create_user_db.save(force_insert=True)
            bot.delete_state(message.from_user.id, message.chat.id)


