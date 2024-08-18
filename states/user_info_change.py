from telebot.handler_backends import State, StatesGroup


class UserInfoChange(StatesGroup):
    name = State()
    polity_city = State()
