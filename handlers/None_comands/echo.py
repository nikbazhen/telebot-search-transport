from loader import bot
from log import logger
from utils.decarated_errors import decorator_error


@bot.message_handler(state=None)
@decorator_error
def get_user_text_and_commands(message):
    """Функция обработки текста и неправильно набранных команд"""
    logger.log_debug('Запуск функции get_user_text_and_commands')
    if str(message.text).startswith('/'):
        bot.send_message(message.chat.id, 'Мне эта команда не известна.\n'
                                          'Откройте меню команд чтобы посмотреть возможные команды')
    elif str(message.text).upper() in ['ПРИВЕТ']:
        bot.send_message(message.chat.id, 'И тебе привет!')
    else:
        bot.send_message(message.chat.id, 'Я тебя не понимаю.')
