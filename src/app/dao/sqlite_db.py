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
    UpdateRateDTO,
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
            float(new_rate.rate)
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
    def get_rate(self, entity: QueryRateDTO) -> GetRateDTO | None:
        base_currency = self.get_currency(QueryCurrencyDTO(entity.base_currency))
        target_currency = self.get_currency(QueryCurrencyDTO(entity.target_currency))
        if base_currency is None or target_currency is None:
            return None
        sql = "SELECT * FROM ExchangeRates WHERE BaseCurrencyId=? AND TargetCurrencyId=?"
        parameters = base_currency.id, target_currency.id
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, parameters)
            rate_data = cursor.fetchone()

        return GetRateDTO(
            id=rate_data[0],
            base_currency=base_currency,
            target_currency=target_currency,
            rate=rate_data[3]
        )

    @override
    def get_all_rate(self) -> list[GetRateDTO]:
        sql = "SELECT * from ExchangeRates"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            rate_data = cursor.fetchall()
            logger.debug(f"Rate data: {rate_data}")
            column_names = ["id", "base_currency", "target_currency", "rate"]
            rate_list_dict = [{key: value for key, value in zip(column_names, rate)} for rate in rate_data]
            for rate in rate_list_dict:
                for key in rate.keys():
                    if key == column_names[1] or key == column_names[2]:
                        cur_id = rate.get(key)
                        cursor.execute(f"SELECT * from Currencies WHERE ID = {cur_id}")
                        rate[key] = GetCurrencyDTO(*cursor.fetchone())

            logger.debug(f"Rate list: {rate_list_dict}")


        res: list[GetRateDTO] = [GetRateDTO(**rate) for rate in rate_list_dict]

        return res

    @override
    def update_rate(self, entity: UpdateRateDTO) -> None:
        base_currency = self.get_currency(QueryCurrencyDTO(entity.base_currency))
        target_currency = self.get_currency(QueryCurrencyDTO(entity.target_currency))
        if base_currency is None or target_currency is None:
            raise ValueError("Currency not found")
        sql = "UPDATE ExchangeRates SET Rate=? WHERE BaseCurrencyId=? AND TargetCurrencyId=?"
        parameters = float(entity.rate), base_currency.id, target_currency.id
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, parameters)
