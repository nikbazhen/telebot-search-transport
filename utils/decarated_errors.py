from telebot.apihelper import ApiHTTPException, ApiTelegramException, ApiException, ApiInvalidJSONException
from loader import bot
import functools
from log import logger


def decorator_error(func):
    """Декоратор обработки ошибок"""
    @functools.wraps(func)
    def wrapper(args, **kwargs):

        try:
            try:
                return func(args, **kwargs)
            except (AttributeError, ApiException, ApiInvalidJSONException,
                    ApiTelegramException, ApiException, ApiHTTPException) as error:
                logger.log_error(str(error))
                bot.send_message(args.chat.id, 'Произошла ошибка Telegram, обработка команды продолжается,'
                                               ' но итог выполнения команды может не дать нужного результата.'
                                               'Если хотите узнать почему произошла эта ошибка, '
                                               'то некоторые примеры возникновения этой ошибки, '
                                               'описаны в команде /help')
        except AttributeError:
            try:
                return func(args, **kwargs)
            except (Exception, ApiException, ApiInvalidJSONException,
                    ApiTelegramException, ApiException, ApiHTTPException) as error:
                logger.log_error(str(error))
                bot.send_message(args.message.chat.id, 'Произошла ошибка Telegram, обработка команды продолжается,'
                                                       ' но итог выполнения команды может не дать нужного результата.'
                                                       'Если хотите узнать почему произошла эта ошибка, '
                                                       'то некоторые примеры возникновения этой ошибки, '
                                                       'описаны в команде /help')
    return wrapper




