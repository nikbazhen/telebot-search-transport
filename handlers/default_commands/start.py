from loader import bot
from database.check_registration_db import check
from database.data import User
from telebot.types import ReplyKeyboardRemove
from keyboards.inline.registration_button import registration_markup
from log import logger
from utils.decarated_errors import decorator_error


@bot.message_handler(commands=['start'])
@decorator_error
def start(message):
    """Функция обработки команды /start"""
    logger.log_debug('Запуск функции start')
    if check(message.from_user.id):
        user = User.select(User.name).where(User.id_user == message.from_user.id)
        user_name = user[0].name
        bot.send_message(message.chat.id, f'Приветствую вас {user_name}', reply_markup=ReplyKeyboardRemove())

    else:
        answer_user = f'Привет!\n' \
                      f'Этот бот предназначен для поиска расписания и цены пригородного и междугородного транспорта на территории РФ,\n'\
                      f'такой как: самолёт, электричка, поезд и автобус.\n' \
                      f'Для того чтобы начать пользоваться ботом, нужно пройти короткую регистрацию.\n' \
                      f'Что бы зарегистрироваться выберите в меню команд, команду "Регистрация в боте", ' \
                      f'либо просто нажмите кнопку ниже:'
        bot.send_message(message.chat.id, answer_user, reply_markup=registration_markup())

