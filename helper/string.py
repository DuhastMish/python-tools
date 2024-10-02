"""
Вспомогтаельные мтеоды для работы со стороками.
"""

import re

from python_utils.helper.datatype import to_str
from python_utils.helper.list import get_elem


def plural_word(value: int, words: list) -> str:
    """
    Получение множественной формы слова.

    :param value:
    :return:
    """
    if all((value % 10 == 1, value % 100 != 11)):
        return get_elem(words, 0, "")
    elif all((2 <= value % 10 <= 4, any((value % 100 < 10, value % 100 >= 20)))):
        return get_elem(words, 1, "")

    return get_elem(words, 2, "")


def remove_spaces(text: str) -> str:
    """
    Удаляет лишние пробелы из строки.

    :param text: Строка с кучей пробелов
    :return: Строка с минимумом пробелов
    """
    return re.sub(' +', ' ', to_str(text))
