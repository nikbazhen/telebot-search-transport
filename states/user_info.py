from telebot.handler_backends import State, StatesGroup


class UserInfo(StatesGroup):
    name = State()
    polity_city = State()
