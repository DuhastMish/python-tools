"""
Класс подключения к базе данных.
"""


from python_utils.db.config import DatabaseConfiguration
from python_utils.logger.main import get_logger

LOGGER = get_logger()


class BaseDatabaseConnector:
    """
    Класс выполнения запросов к базе данных.
    """

    def __init__(self):
        self.host = DatabaseConfiguration.HOST
        self.username = DatabaseConfiguration.USERNAME
        self.password = DatabaseConfiguration.PASSWORD
        self.port = DatabaseConfiguration.PORT
        self.dbname = DatabaseConfiguration.NAME
