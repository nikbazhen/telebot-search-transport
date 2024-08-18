from telebot.types import BotCommand
from config_data.config import COMMANDS


def set_commands(bot):
    """Функция создания меню команд в Telegram"""
    bot.set_my_commands([BotCommand(*i) for i in COMMANDS])
