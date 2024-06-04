"""
Логирует текущий фрейм.
"""
import inspect

from lib.logger.main import get_logger

LOGGER = get_logger()


def log_current_frame():
    """
    Логирует текущий фрейм по формату.
    D:/AyeBot/lib/logger/frame.py:39
    D:/AyeBot/lib/logger/main.py:63
    """
    logging_block_name = "[Python Stack]"

    LOGGER.error(logging_block_name)

    # Разворачиваем список и удаляем последний вызов (log_current_frame)
    for call_frame in inspect.stack()[:0:-1]:
        LOGGER.error(f"{call_frame.filename}:{call_frame.lineno}")

    LOGGER.error(logging_block_name)
