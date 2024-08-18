from database.data import User
from log import logger


def check(id_key: int) -> bool:
    """
    Функция для проверки есть ли пользователь в базе данных.
    :param id_key: Id пользователя.
    :return: Булевое значение.
    """
    logger.log_debug('Запуск функции check')
    try:
        User.get(User.id_user == id_key)
        return True
    except User.DoesNotExist:
        return False

