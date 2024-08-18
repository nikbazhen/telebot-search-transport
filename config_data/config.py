import os
from dotenv import find_dotenv, load_dotenv
from log import logger

logger.log_debug('Запуск файла config.py')

if find_dotenv():
    load_dotenv()
else:
    logger.log_error('Error processing message: Файл ".env", не найден!')
    raise Exception('Файл ".env", не найден!\nСоздайте файл ".env" с переменными окружения("TOKEN"; "API_KEY")')

TOKEN = os.getenv('TOKEN')
if TOKEN is None:
    logger.log_error('Error processing message: Отсутствует токен Telebot.')
    raise Exception('Отсутствует токен Telebot.')
KEY_API_SCHEDULE = os.getenv('KEY_API_SCHEDULE')
if KEY_API_SCHEDULE is None:
    logger.log_error('Error processing message: Отсутствует токен Яндекс.Расписания.')
    raise Exception('Отсутствует токен Яндекс.Расписания.')
KEY_API_GEOLOCATION = os.getenv('KEY_API_GEOLOCATION')
if KEY_API_GEOLOCATION is None:
    logger.log_error('Error processing message: Отсутствует токен Яндекс.Геокодер.')
    raise Exception('Отсутствует токен Яндекс.Геокодер.')
COMMANDS = (
    ('start', 'Запуск бота'),
    ('help', 'Справка по боту'),
    ('registration', 'Регистрация в боте'),
    ('changing_credentials', 'Изменение учётных данных'),
    ('route_search', 'Поиск маршрутов'),
    ('history', 'Посмотреть историю'),
    ('low', 'Поиск самого дешёвого маршрута'),
    ('high', 'Поиск самого дорогого маршрута'),
    ('custom', 'Поиск маршрута в заданном диапазоне')
)

