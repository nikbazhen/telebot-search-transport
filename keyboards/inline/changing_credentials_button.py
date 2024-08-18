from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import bot
from utils.decarated_errors import decorator_error
from log import logger


def changing_credentials_markup():
    """Inline кнопка"""
    logger.log_debug('Запуск функции inline кнопки changing_credentials_markup')
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Перезаписать персональные данные', callback_data='changing_credentials'))
    return markup


@bot.callback_query_handler(func=lambda call: call.data == 'changing_credentials')
@decorator_error
def changing_credentials_callback(callback):
    """Функция-обработчик inline кнопки"""
    logger.log_debug('Запуск функции-обработчика changing_credentials_callback, inline кнопки')
    from handlers.custom_commands.changing_credentials import registration1
    registration1(callback.message)