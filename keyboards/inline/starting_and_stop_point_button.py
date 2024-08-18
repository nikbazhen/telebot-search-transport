from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import bot
from utils.global_variables import GlobalVariables
import math
from utils.decarated_errors import decorator_error
from log import logger


def starting_and_stop_point_button(dict_station, switch):
    """Inline кнопка"""
    logger.log_debug('Запуск функции inline кнопки starting_and_stop_point_button')
    GlobalVariables.glob_dict_station = dict_station
    GlobalVariables.count = len(dict_station)
    GlobalVariables.switch_start_and_stop = switch
    GlobalVariables.page = int(math.ceil(GlobalVariables.count / 9))
    markup = InlineKeyboardMarkup()
    for i in list(GlobalVariables.glob_dict_station.items())[:9]:
        markup.add(InlineKeyboardButton(f'{i[1][1]}', callback_data=f'sr_sp{i[0]}'))
    if GlobalVariables.page > 1:
        markup.add(InlineKeyboardButton(f'1/{GlobalVariables.page}', callback_data='sr_spCurrent_page'),
                   InlineKeyboardButton('Вперёд >>>', callback_data='sr_spNext_page'))

    return markup


@bot.callback_query_handler(func=lambda call: call.data.startswith('sr_sp'))
@decorator_error
def callback_start_stop(callback):
    """Функция-обработчик inline кнопки"""
    logger.log_debug('Запуск функции-обработчика callback_start_stop, inline кнопки')
    if callback.data != 'sr_spNext_page' and callback.data != 'sr_spBack_page' and callback.data != 'sr_spCurrent_page':

        bot.edit_message_text(f'Вы выбрали: {GlobalVariables.glob_dict_station[callback.data[5:]][1]}',
                              reply_markup=None,
                              chat_id=callback.message.chat.id,
                              message_id=callback.message.message_id)
        if GlobalVariables.switch_start_and_stop == 'start':
            from handlers.custom_commands.route_search import starting_point
            starting_point(callback.message, answer=GlobalVariables.glob_dict_station[callback.data[5:]],
                           check_button=True)
        elif GlobalVariables.switch_start_and_stop == 'stop':
            from handlers.custom_commands.route_search import stop_point
            stop_point(callback.message, answer=GlobalVariables.glob_dict_station[callback.data[5:]],
                       check_button=True)
    if callback.data == 'sr_spNext_page':
        GlobalVariables.current_page += 1
        markup = InlineKeyboardMarkup()
        for i in list(GlobalVariables.glob_dict_station.items())[
                 9 * GlobalVariables.current_page - 9:9 * GlobalVariables.current_page + 1]:
            markup.add(InlineKeyboardButton(f'{i[1][1]}', callback_data=f'sr_sp{i[0]}'))
        if GlobalVariables.current_page == GlobalVariables.page:
            markup.add(InlineKeyboardButton('<<< Назад', callback_data='sr_spBack_page'),
                       InlineKeyboardButton(f'{GlobalVariables.current_page}/{GlobalVariables.page}',
                                            callback_data='sr_spCurrent_page'))
        else:
            markup.add(InlineKeyboardButton('<<< Назад', callback_data='sr_spBack_page'),
                       InlineKeyboardButton(f'{GlobalVariables.current_page}/{GlobalVariables.page}',
                                            callback_data='sr_spCurrent_page'),
                       InlineKeyboardButton('Вперёд >>>', callback_data='sr_spNext_page'))
        bot.edit_message_text(f'страница {GlobalVariables.current_page} из {GlobalVariables.page}', reply_markup=markup,
                              chat_id=callback.message.chat.id, message_id=callback.message.message_id)

    elif callback.data == 'sr_spBack_page':
        GlobalVariables.current_page -= 1
        markup = InlineKeyboardMarkup()
        for i in list(GlobalVariables.glob_dict_station.items())[
                 9 * GlobalVariables.current_page - 9:9 * GlobalVariables.current_page + 1]:
            markup.add(InlineKeyboardButton(f'{i[1][1]}', callback_data=f'sr_sp{i[0]}'))
        if GlobalVariables.current_page == 1:
            markup.add(InlineKeyboardButton(f'1/{GlobalVariables.page}', callback_data='sr_spCurrent_page'),
                       InlineKeyboardButton('Вперёд >>>', callback_data='sr_spNext_page'))
        else:
            markup.add(InlineKeyboardButton('<<< Назад', callback_data='sr_spBack_page'),
                       InlineKeyboardButton(f'{GlobalVariables.current_page}/{GlobalVariables.page}',
                                            callback_data='sr_spCurrent_page'),
                       InlineKeyboardButton('Вперёд >>>', callback_data='sr_spNext_page'))
        bot.edit_message_text(f'страница {GlobalVariables.current_page} из {GlobalVariables.page}', reply_markup=markup,
                              chat_id=callback.message.chat.id, message_id=callback.message.message_id)
