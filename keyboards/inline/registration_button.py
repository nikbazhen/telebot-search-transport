from loader import bot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.decarated_errors import decorator_error
from log import logger


def registration_markup():
    """Inline кнопка"""
    logger.log_debug('Запуск функции inline кнопки starting_and_stop_point_buttonregistration_markup')
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Пройти регистрацию', callback_data='registration'))
    return markup


@bot.callback_query_handler(func=lambda call: call.data == 'registration')
@decorator_error
def registration_callback(callback):
    """Функция-обработчик inline кнопки"""
    logger.log_debug('Запуск функции-обработчика registration_callback, inline кнопки')
    from handlers.custom_commands.registration import registration
    registration(callback.message)

