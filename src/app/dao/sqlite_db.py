import logging
import sqlite3
from pathlib import Path
from sqlite3 import Connection

from app.dao import DatabaseManager


logger = logging.getLogger(__name__)


class SQLiteManager(DatabaseManager):
    """SQLite connector"""
    def __init__(self, db_path: Path) -> None:
        self.path = db_path

    def _get_connection(self) -> Connection:
        logger.debug(f'Path to database: {self.path}')
        logger.debug(f'Path to run module: {__file__}')
        return sqlite3.connect(self.path)

    def add_currency[T](self, new_currency: T ):
        sql = "INSERT INTO Currencies (Code, FullName, Sign) VALUES (?, ?, ?)"
        parameters = (
            new_currency.currency_code,
            new_currency.full_name,
            new_currency.sign
        )
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, parameters)

    def add_rate(self, new_rate):
        sql = '''INSERT INTO ExchangeRates (BaseCurrencyId, TargetCurrencyId, Rate) 
                        VALUES (
                        (SELECT ID FROM Currencies WHERE Code == ?), 
                        (SELECT ID FROM Currencies WHERE Code == ?), 
                        ?)'''
        parameters = (
            new_rate.base_currency,
            new_rate.target_currency,
            new_rate.rate
        )
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, parameters)

    def get_currency(self, entity):
        sql = "SELECT * from Currencies WHERE Code = ?"
        parameters = entity
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, parameters)
            currency_data = cursor.fetchone()

        return currency_data

    def get_rate(self, entity):
        pass

    def update_rate(self, entity):
        pass

    def update_currency(self, entity):
        pass


