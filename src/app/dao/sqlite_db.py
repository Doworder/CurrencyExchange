import logging
import sqlite3
from pathlib import Path
from sqlite3 import Connection
from typing import override

from app.dao import DatabaseManager
from app.dto import (
    GetCurrencyDTO,
    GetRateDTO,
    AddCurrencyDTO,
    AddRateDTO,
    QueryCurrencyDTO,
    QueryRateDTO,
)

logger = logging.getLogger(__name__)


class SQLiteManager(DatabaseManager):
    """SQLite connector"""
    def __init__(self, db_path: Path) -> None:
        self.path = db_path

    def _get_connection(self) -> Connection:
        logger.debug(f'Path to database: {self.path}')
        logger.debug(f'Path to run module: {__file__}')
        return sqlite3.connect(self.path)

    @override
    def add_currency(self, new_currency: AddCurrencyDTO) -> None:
        sql = "INSERT INTO Currencies (Code, FullName, Sign) VALUES (?, ?, ?)"
        parameters = (
            new_currency.currency_code,
            new_currency.full_name,
            new_currency.sign
        )
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, parameters)

    @override
    def add_rate(self, new_rate: AddRateDTO) -> None:
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

    @override
    def get_currency(self, entity: QueryCurrencyDTO) -> GetCurrencyDTO | None:
        sql = "SELECT * from Currencies WHERE Code = ?"
        parameters = entity.currency_code,
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, parameters)
            currency_data = cursor.fetchone()
            if currency_data is None:
                return currency_data

        return GetCurrencyDTO(*currency_data)

    @override
    def get_all_currency(self) -> list[GetCurrencyDTO]:
        sql = "SELECT * from Currencies"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            currency_data = cursor.fetchall()

        res: list[GetCurrencyDTO] = [GetCurrencyDTO(*currency) for currency in currency_data]

        return res

    @override
    def get_rate(self, entity: QueryRateDTO) -> GetRateDTO:
        pass

    @override
    def get_all_rate(self) -> list[GetRateDTO]:
        pass

    @override
    def update_rate(self, entity: GetRateDTO) -> None:
        pass

    @override
    def update_currency(self, entity: GetCurrencyDTO) -> None:
        pass
