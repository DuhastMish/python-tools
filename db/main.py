"""
Класс подключения к базе данных.
"""


import psycopg2
from psycopg2.extras import RealDictCursor

from python_utils.db.base import BaseDatabaseConnector
from python_utils.helper.list import get_first_elem
from python_utils.helper.string import remove_spaces
from python_utils.logger.main import get_logger, log_method

LOGGER = get_logger()


class DatabaseConnector(BaseDatabaseConnector):
    """
    Класс выполнения запросов к базе данных.
    """

    def __init__(self):
        super().__init__()

        self._conn = None

    @property
    def connection(self) -> psycopg2.extensions.connection:
        """
        Возвращает подключение к БД.
        """
        if self._conn is None:
            self.__set_connection()
        return self._conn

    @log_method
    def select(self, query):
        """
        Выполняет запрос SELECT.
        """
        with self.connection as conn:
            with conn.cursor() as cursor:
                try:
                    LOGGER.debug(remove_spaces(query))
                    cursor.execute(query)
                    record_set = list(cursor.fetchall())
                    return record_set
                except Exception as ex:
                    LOGGER.warn(f"{query}")
                    LOGGER.fatal(f"Error executing SQL: {ex}")
                    raise ex

    @log_method
    def select_as_dict(self, query) -> list[dict]:
        """
        Выполняет запрос SELECT и возвращает результат в виде списока словарей.
        """
        with self.connection as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                try:
                    LOGGER.debug(remove_spaces(query))
                    cursor.execute(query)
                    record_set = cursor.fetchall()
                    LOGGER.debug(f"RESULT (select_as_dict): {record_set}")
                    return record_set
                except Exception as ex:
                    LOGGER.warn(f"{query}")
                    LOGGER.fatal(f"Error executing SQL: {ex}")
                    raise ex

    @log_method
    def execute(self, query):
        """
        Выполняет запрос без возврата значения.
        """
        with self.connection as conn:
            with conn.cursor() as cursor:
                try:
                    LOGGER.debug(remove_spaces(query))
                    cursor.execute(query)
                except Exception as ex:
                    LOGGER.warn(f"{query}")
                    LOGGER.fatal(f"Error executing SQL: {ex}")
                    raise ex

    @log_method
    def fetchone(self, query):
        """
        Выполняет запрос возвращает единственное значение.
        """
        with self.connection as conn:
            with conn.cursor() as cursor:
                try:
                    LOGGER.debug(remove_spaces(query))
                    cursor.execute(query)
                    record_set = cursor.fetchone()
                    elem = get_first_elem(record_set)
                    LOGGER.debug(f"RESULT fetchone: {elem}")
                    return elem
                except Exception as ex:
                    LOGGER.warn(f"{query}")
                    LOGGER.fatal(f"Error executing SQL: {ex}")
                    raise ex

    def __set_connection(self) -> None:
        """
        Открывает подключение к БД.
        """
        try:
            self._conn = psycopg2.connect(
                host=self.host,
                user=self.username,
                password=self.password,
                port=self.port,
                dbname=self.dbname,
            )
        except psycopg2.DatabaseError as ex:
            LOGGER.critical("Ошибка подключения к БД", exc_info=True)
            raise ex
        finally:
            LOGGER.info(f"Подключение к БД {self.host}:{self.port}.")


database = DatabaseConnector()
