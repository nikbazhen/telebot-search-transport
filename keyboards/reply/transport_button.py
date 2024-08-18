from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from log import logger


def transport_markup():
    """Reply кнопка"""
    logger.log_debug('Запуск функции reply кнопки transport_markup')
    markup = ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add(KeyboardButton('Самолёт'))
    markup.add(KeyboardButton('Поезд'))
    markup.add(KeyboardButton('Электричка'))
    markup.add(KeyboardButton('Автобус'))
    return markup
