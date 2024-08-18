from loader import bot
from handlers.custom_commands.route_search import route_search
from database.check_registration_db import check
from utils.switch_bool import SwitchBool
from log import logger
from utils.decarated_errors import decorator_error


@bot.message_handler(commands=['low'])
@decorator_error
def filter_low(message):
    """Функция обработки команды /low"""
    logger.log_debug('Запуск функции filter_low')
    if check(message.chat.id):
        SwitchBool.low_filt = True
        route_search(message)
    else:
        bot.send_message(message.chat.id, 'Для использования этой команды необходимо пройти регистрацию!')
