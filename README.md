
# Телеграм-бот поиска расписания и цены пригородного и междугородного транспорта на территории РФ.

### Реализованные команды:
1) /start
2) /help
3) /changing_credentials
4) /custom
5) /high
6) /history
7) /low
8) /registration
9) /route_search

low, high, custom выполняют поиск с сортировкой соответственно по минимальной цене, максимальной цене и по-указанному диапазону цен.

Команда route_search выполняет общий поиск.

Команда history отвечает за просмотр последних 10 результатов поиска.

Команда registration отвечает за регистрацию пользователя.

Команда changing_credentials отвечает за изменение учётных данных.

Команда help отвечает за вызов инструкции для пользователя.

Без регистрации пользователя, бот будет отправлять на регистрацию или выведет сообщение, что нужно зарегистрироваться.

Для запуска бота необходимо создать файл .env, по образцу .env.template, а так же необхадимо установить все зависимости из файла requirements.txt.


