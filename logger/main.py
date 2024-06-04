"""
Method logger.
"""

import logging
import shutil
import time
from datetime import datetime
from functools import wraps
from http.client import HTTPConnection
from pathlib import Path
from typing import Any, Callable, ParamSpec, TypeVar

from python_utils.helper.datetime import MILISECONDS_IN_SECOND, date_to_str

CALL_BEGIN = 'Method call "{method}".'
CALL_ERROR = 'Error while executing "{method}":\n\r{trace}'
CALL_RESULT = 'Method "{method}" executed in "{time}" ms.'

P = ParamSpec("P")
T = TypeVar("T")

LOG_FILE_NAME = f"{date_to_str(datetime.now())}.log"
LOG_FOLDER = "logs"
LOG_ENCODING = "utf-8"
LOG_PATH = Path(Path.cwd() / LOG_FOLDER)


def _init_logger():
    """
    Init logger.
    """
    log_level = logging.INFO

    LOG_PATH.mkdir(parents=True, exist_ok=True)
    HTTPConnection.debuglevel = 1
    logging.basicConfig(
        level=log_level,
        filename=f"{LOG_FOLDER}/{LOG_FILE_NAME}",
        encoding=LOG_ENCODING,
        format="%(filename)s:%(lineno)d #%(levelname)-8s "
        "[%(asctime)s] - %(name)s - %(message)s",
    )
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(log_level)
    requests_log.propagate = True

    uvicorn_logger = logging.getLogger("aiogram")
    uvicorn_logger.propagate = True
    uvicorn_logger.setLevel(logging.WARNING)

    uvicorn_logger = logging.getLogger("uvicorn")
    uvicorn_logger.propagate = True
    uvicorn_logger.setLevel(log_level)

    uvicorn_access_logger = logging.getLogger("uvicorn.access")
    uvicorn_access_logger.propagate = True
    uvicorn_access_logger.setLevel(log_level)

    uvicorn_error_logger = logging.getLogger("uvicorn.error")
    uvicorn_error_logger.propagate = True
    uvicorn_error_logger.setLevel(log_level)


def get_logger():
    """
    Get logger.
    """
    _init_logger()
    return logging.getLogger(__name__)


def log_method(func: Callable[P, T] | None = None) -> Callable[P, T]:
    """
    Method log decorator.
    """

    def decorate(function: Callable[P, T]) -> Callable[P, T]:
        @wraps(function)
        def log_wrapper(*args: P.args, **kwargs: P.kwargs) -> Any:
            function_name = function.__name__
            logger = get_logger()
            func_result = None
            start_time = time.time()
            try:
                logger.debug(CALL_BEGIN.format(method=function_name))
                func_result = function(*args, **kwargs)
            except Exception as ex:
                logger.error(CALL_ERROR.format(method=function_name, trace=str(ex)))
                raise
            finally:
                execution_time = (time.time() - start_time) * MILISECONDS_IN_SECOND
                logger.debug(CALL_RESULT.format(method=function_name, time=str(round(execution_time, 5))))

            return func_result

        return log_wrapper

    return decorate(func) if func is not None else decorate


async def zip_logs() -> Path:
    """
    Zip logs.
    """
    shutil.make_archive("logs", "zip", str(LOG_PATH))
    return "./logs.zip"
