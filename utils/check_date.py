import datetime
import timezonefinder
import pytz
from log import logger


def check_date(text_date: str, lat: float, lng: float) -> bool:
    """Функция для проверки даты и времени, введённой пользователем."""
    logger.log_debug('Запуск функции check_date')
    try:
        date_obj = datetime.date.fromisoformat(text_date)
        tf = timezonefinder.TimezoneFinder()
        timezone_str = tf.certain_timezone_at(lat=lat, lng=lng)
        timezone = pytz.timezone(timezone_str)
        dt = datetime.datetime.utcnow()
        date_is_now = str(dt + timezone.utcoffset(dt))[:10]
        date_obj_2 = datetime.date.fromisoformat(date_is_now)
        if date_obj >= date_obj_2:
            return True
        else:
            return False
    except ValueError:
        return False
