"""
Класс подключения к базе данных.
"""

import psycopg
from psycopg.rows import dict_row

from python_utils.db.base import BaseDatabaseConnector
from python_utils.helper.string import remove_spaces
from python_utils.logger.main import get_logger, log_method

LOGGER = get_logger()


class AsyncDatabaseConnector(BaseDatabaseConnector):
    """
    Класс выполнения запросов к базе данных.
    """

    def __init__(self):
        super().__init__()

        self._connection_kwargs = {
            "host": self.host,
            "user": self.username,
            "password": self.password,
            "port": self.port,
            "dbname": self.dbname,
            "row_factory": dict_row,
        }

    @log_method
    async def select(self, query, db_schema: str | None = None) -> list[dict]:
        """
        Выполняет запрос SELECT и возвращает результат в виде списока словарей.
        """
        aconn = await psycopg.AsyncConnection.connect(**self._connection_kwargs)
        async with aconn:
            async with aconn.cursor() as cursor:
                try:
                    LOGGER.debug(remove_spaces(query))
                    if db_schema:
                        await cursor.execute("SET search_path TO " + db_schema)
                    await cursor.execute(query)
                    record_set = await cursor.fetchall()
                    LOGGER.debug(f"RESULT (select): {record_set}")
                    return record_set
                except Exception as ex:
                    LOGGER.warn(f"{query}")
                    LOGGER.fatal(f"Error executing SQL: {ex}")
                    raise ex

        await aconn.close()

    @log_method
    async def execute(self, query: str, db_schema: str | None = None):
        """
        Выполняет запрос без возврата значения.
        """
        aconn = await psycopg.AsyncConnection.connect(**self._connection_kwargs)
        async with aconn:
            async with aconn.cursor() as cursor:
                try:
                    LOGGER.debug(remove_spaces(query))
                    if db_schema:
                        await cursor.execute("SET search_path TO " + db_schema)
                    await cursor.execute(query)
                except Exception as ex:
                    LOGGER.warn(f"{query}")
                    LOGGER.fatal(f"Error executing SQL: {ex}")
                    raise ex

        await aconn.close()

    @log_method
    async def select_one(self, query, db_schema: str | None = None):
        """
        Выполняет запрос возвращает единственное значение.
        """
        aconn = await psycopg.AsyncConnection.connect(**self._connection_kwargs)
        async with aconn:
            async with aconn.cursor() as cursor:
                try:
                    LOGGER.debug(remove_spaces(query))
                    if db_schema:
                        await cursor.execute("SET search_path TO " + db_schema)
                    await cursor.execute(query)
                    record = await cursor.fetchone()
                    LOGGER.debug(f"RESULT fetchone: {record}")
                    return record
                except Exception as ex:
                    LOGGER.warn(f"{query}")
                    LOGGER.fatal(f"Error executing SQL: {ex}")
                    raise ex

        await aconn.close()


async_database = AsyncDatabaseConnector()
