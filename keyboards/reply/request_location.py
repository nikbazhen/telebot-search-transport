from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from log import logger


def request_location():
    """Reply кнопка"""
    logger.log_debug('Запуск функции reply кнопки request_location')
    markup = ReplyKeyboardMarkup(True, one_time_keyboard=True,)
    markup.add(KeyboardButton('Поделиться местоположением', request_location=True))
    return markup
