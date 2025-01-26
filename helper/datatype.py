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

    return result


def to_str(value: Any) -> str:
    """
    Очистить строку - удалить пробелы в начале и конце.
    :param value:
    :return:
    """
    return str(value).strip() if value is not None else ""


def as_array(value, force: bool = True) -> list:
    """
    Привести значение к списку.
    :param value: исходное значение
    :param force: пропускать значенние, если невозможно привести к типу
    :return:
    """
    if isinstance(value, (list, tuple, set)):
        return list(value)
    elif value is None and force:
        return []
    else:
        return [value]


def to_array(value, to_type: type = None, force: bool = False) -> list:
    """
    Привести значение к массиву (определенного типа).
    :param value: исходное значение
    :param to_type: тип
    :type to_type: type
    :param force: пропускать значенние, если невозможно привести к типу
    """
    result = as_array(value)
    result = list_cast(result, to_type, force)
    return result


def list_cast(value: list, to_type: type, force: bool = False) -> list:
    """
    Приведение элементов списка к определенному типу.
    :param value: список
    :param to_type: тип
    :type to_type: type
    :param force: пропускать значения, которые не получается привести
    """
    if not to_type:
        return value

    result = []
    for item in value:
        try:
            item = cast(item, to_type)
            result.append(item)
        except Exception:
            if not force:
                raise

    return result


def cast(value, to_type: type):
    """
    Приведение к нужному типу
    :param value: исходное значение
    :param to_type: тип
    :type to_type: type
    """
    try:
        value = to_type(value)
    except (ValueError, TypeError):
        raise

    return value
