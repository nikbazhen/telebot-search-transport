from loader import bot
from utils.set_commands import set_commands
from telebot.custom_filters import StateFilter, IsDigitFilter
from database.data import create_models
from handlers import custom_commands
from handlers import default_commands
from handlers import None_comands
from telebot.apihelper import ApiHTTPException, ApiTelegramException, ApiException, ApiInvalidJSONException
from log import logger


try:
    if __name__ == '__main__':
        create_models()
        bot.add_custom_filter(StateFilter(bot))
        bot.add_custom_filter(IsDigitFilter())
        set_commands(bot)
        bot.infinity_polling(none_stop=True)
except (Exception, ApiException, ApiInvalidJSONException, ApiTelegramException, ApiException, ApiHTTPException) as error:
    logger.log_error(str(error))

