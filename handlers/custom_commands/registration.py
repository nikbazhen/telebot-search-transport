from keyboards.reply.request_location import request_location
from states.user_info import UserInfo
from utils.working_with_the_yandex_api.address_from_coords import get_address
from loader import bot
from database.data import User
from database.check_registration_db import check
from keyboards.inline.help_button import help_button
from telebot.types import ReplyKeyboardRemove
from log import logger
from utils.decarated_errors import decorator_error


@bot.message_handler(commands=['registration'])
@decorator_error
def registration(message):
    """Функция обработки команды /registration"""
    logger.log_debug('Запуск функции registration')
    if check(message.chat.id):
        from keyboards.inline.changing_credentials_button import changing_credentials_markup
        bot.send_message(message.chat.id, 'Вы уже зарегистрированы в боте!\n'
                                          'Если вы хотите изменить вашу текущую учётную запить,'
                                          ' выберите в меню выберите в меню команд, команду "Изменение учётных данных", '
                                          'либо просто нажмите кнопку ниже:', reply_markup=changing_credentials_markup())
    else:

        bot.set_state(message.chat.id, UserInfo.name, message.chat.id)
        bot.send_message(message.chat.id, 'Введите ваше имя',  reply_markup=ReplyKeyboardRemove())


@bot.message_handler(state=UserInfo.name)
@decorator_error
def get_name(message):
    """Функция обработки состояния UserInfo.name"""
    logger.log_debug('Запуск функции get_name')
    if message.text.isalpha():
        bot.set_state(message.chat.id, UserInfo.polity_city, message.chat.id)
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


@bot.message_handler(content_types=['location', 'text'], state=UserInfo.polity_city)
@decorator_error
def get_polity_city(message):
    """Функция обработки состояния UserInfo.name"""
    logger.log_debug('Запуск функции get_polity_city')
    if message.content_type == 'location':
        longitude = str(message.location.longitude)
        latitude = str(message.location.latitude)
        geo = get_address(longitude, latitude)
        with bot.retrieve_data(message.chat.id, message.chat.id) as data:
            data['polity_city'] = geo
            bot.send_message(message.chat.id, 'Регистрация данных прошла успешно!', reply_markup=ReplyKeyboardRemove())
            bot.send_message(message.chat.id,
                                            f'Вот ваши данные:\n'
                                            f'Имя - {data["name"]}\n'
                                            f'Местоположение - {data["polity_city"]},\n'
                                            f'Для того что бы вам было понятно, как работать с ботом выберите в'
                                            f' меню команд, команду "Справка по боту", либо нажмите на'
                                            f' кнопку ниже:',
                             reply_markup=help_button())
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
                bot.send_message(message.chat.id, 'Регистрация данных прошла успешно!',
                                 reply_markup=ReplyKeyboardRemove())
                bot.send_message(message.chat.id,
                                                f'Вот ваши данные:\n'
                                                f'Имя - {data["name"]}\n'
                                                f'Местоположение - {data["polity_city"]},\n'
                                                f'Для того что бы вам было понятно, '
                                                f'как работать с ботом выберите в'
                                                f' меню команд, команду "Справка по боту", либо нажмите на'
                                                f' кнопку ниже:',
                                 reply_markup=help_button())
                create_user_db = User(id_user=message.chat.id, name=data['name'], polity_city=data['polity_city'],
                                      latitude_adress=geo[1][1], longitude_adress=geo[1][0])
                create_user_db.save(force_insert=True)
            bot.delete_state(message.from_user.id, message.chat.id)







