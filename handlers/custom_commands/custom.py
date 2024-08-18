from loader import bot
from handlers.custom_commands.route_search import route_search
from database.check_registration_db import check
from utils.global_variables import GlobalVariables
from log import logger
from utils.decarated_errors import decorator_error


@bot.message_handler(commands=['custom'])
@decorator_error
def filter_custom(message):
    """Функция обработки команды /custom"""
    logger.log_debug('Запуск функции filter_custom')
    if check(message.chat.id):
        msg = bot.send_message(message.chat.id, 'Введите начальную и конечную сумму через "-".\nНапример: 100-1000')
        bot.register_next_step_handler(msg, check_custom)
    else:
        bot.send_message(message.chat.id, 'Для использования этой команды необходимо пройти регистрацию!')


@decorator_error
def check_custom(message):
    """Функция для проверки правильности ввода диапазона цен."""
    logger.log_debug('Запуск функции check_custom')
    text = message.text.split('-')
    try:
        str = int(text[0])
        stp = int(text[1])
        if stp < str or str < 0:
            raise ValueError
        GlobalVariables.custom_filt = [str, stp]
        route_search(message)
    except (ValueError, IndexError):
        msg = bot.send_message(message.chat.id, 'Ошибка ввода.\nНачальная и конечна сумма должны быть числом'
                                                ' и должны указаны через "-", а так же конечная стоимость'
                                                ' не должна быть меньше начальной стоимости и '
                                                'начальная стоимость не должна быть меньше нуля.\nНапример: 100-1000')
        bot.register_next_step_handler(msg, filter_custom)




