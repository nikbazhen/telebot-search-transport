from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import bot
from utils.decarated_errors import decorator_error
from log import logger


def help_button():
    """Inline кнопка"""
    logger.log_debug('Запуск функции inline кнопки help_button')
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Помощь по командам', callback_data='help'))
    return markup


@bot.callback_query_handler(func=lambda call: call.data == 'help')
@decorator_error
def help_callback(callback):
    """Функция-обработчик inline кнопки"""
    logger.log_debug('Запуск функции-обработчика help_callback, inline кнопки')
    from handlers.default_commands.help import reference
    reference(callback.message)
