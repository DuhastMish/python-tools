"""
Модуль для работы со временем.
"""
from datetime import datetime

DEFAULT_DATE_FORMAT = "%Y-%m-%d"
DEFAULT_TIME_FORMAT = "%H:%M:%S"
DEFAULT_DATETIME_FORMAT = f"{DEFAULT_DATE_FORMAT} {DEFAULT_TIME_FORMAT}"

DAYS_IN_WEEK = 7
DAYS_IN_MONTH = 30
MINUTES_IN_HOUR = 60
HOURS_IN_DAYS = 24

MILISECONDS_IN_SECOND = 1000


def date_to_str(value: datetime, format_=DEFAULT_DATE_FORMAT) -> str | None:
    """
    Преобразование date к строке

    :param value:
    :param format_:
    :return:
    """
    try:
        return value.strftime(format_)
    except AttributeError:
        return None


def str_to_date(value, format_=DEFAULT_DATE_FORMAT) -> datetime | None:
    """
    Преобразование строки к date

    :param value:
    :param format_:
    :return:
    """
    try:
        return datetime.strptime(value, format_)
    except Exception:
        return None
