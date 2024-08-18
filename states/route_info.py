from telebot.handler_backends import State, StatesGroup


class RouteInfo(StatesGroup):
    transport = State()
    starting_point = State()
    stop_point = State()
    date = State()
    stop_func = State()

