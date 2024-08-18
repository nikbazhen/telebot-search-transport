from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
from loader import bot
from utils.decarated_errors import decorator_error
from log import logger


@bot.callback_query_handler(func=DetailedTelegramCalendar.func())
@decorator_error
def callback_calendar(callback):
    """Inline кнопка, из сторонней библиотеки"""
    logger.log_debug('Запуск функции inline кнопки callback_calendar')
    result, key, step = DetailedTelegramCalendar(locale='ru').process(callback.data)
    if not result and key:
        bot.edit_message_text(f"Выберите {LSTEP[step][0]}:",
                              callback.message.chat.id,
                              callback.message.message_id,
                              reply_markup=key)
    elif result:
        from handlers.custom_commands.route_search import departure_date
        bot.edit_message_text(f"Вы выбрали дату: {result}",
                              callback.message.chat.id,
                              callback.message.message_id)
        departure_date(callback.message, answer=str(result), check_button=True)
