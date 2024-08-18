import telebot
from telebot.storage import StateMemoryStorage
from config_data.config import TOKEN


storage = StateMemoryStorage()
bot = telebot.TeleBot(TOKEN, state_storage=storage)
