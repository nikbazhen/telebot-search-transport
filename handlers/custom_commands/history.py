from loader import bot
from database.data import History
from log import logger
from utils.decarated_errors import decorator_error


@bot.message_handler(commands=['history'])
@decorator_error
def history(message):
    """Функция обработки команды /history"""
    logger.log_debug('Запуск функции history')
    answer = ''
    records = History.select().where(History.id_user == message.chat.id)
    if records:
        for i in records:
            answer += '=' * 20 + '\n'
            answer += (f'{i.transport}\n'
                       f'{i.start}\n'
                       f'{i.stop}\n'
                       f'{i.date}\n'
                       f'{i.search_parameter}\n'
                       f'{i.result}\n'
                       f'{i.date_search}\n')
            answer += '=' * 20 + '\n'
        bot.send_message(message.chat.id, answer)
    else:
        bot.send_message(message.chat.id, 'В истории нету записей.')
