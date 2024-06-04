"""
Безопасные методы по приведению типов.
"""

from typing import Any

from python_utils.logger.frame import log_current_frame
from python_utils.logger.main import get_logger

LOGGER = get_logger()


def to_float(value: Any, round_to: int = None) -> float | None:
    """
    Привести строку к float.
    :param value:
    :param round_to: округлить до заданного количества разрядов (в случае необходимости)
    :return:
    """
    result = None

    if not value:
        return result

    try:
        value.replace(",", ".") if isinstance(value, str) else None
        value = float(value)
        result = round(value, round_to) if round_to else value
    except Exception as ex:
        LOGGER.error(f"Не удалось привести строку к float: {ex}", exc_info=True)
        log_current_frame()

    return result


def to_int(value: Any) -> int | None:
    """
    Привести строку к int.
    :param value:
    :return:
    """
    result = None

    if value is None:
        return result

    try:
        value = value.replace(" ", "") if isinstance(value, str) else value
        result = int(value)
    except Exception as ex:
        LOGGER.error(f"Не удалось привести строку к int: {ex}", exc_info=True)
        log_current_frame()

    return result


def to_str(value: Any) -> str:
    """
    Очистить строку - удалить пробелы в начале и конце
    :param value:
    :return:
    """
    return str(value).strip() if value is not None else ""
