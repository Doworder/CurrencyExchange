import sqlite3
from pathlib import Path
from sqlite3 import Connection

from src.app.dao import DatabaseManager


class SQLiteManager(DatabaseManager):
    """SQLite connector"""
    def __init__(self, db_path: Path) -> None:
        self.path = db_path

    def _get_connection(self) -> Connection:
        return sqlite3.connect(self.path)

    def add_currency(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Currencies (Code, FullName, Sign) VALUES (?, ?, ?)",
                ("1", "1", "1")
            )

    def add_rate(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO ExchangeRates (BaseCurrencyId, TargetCurrencyId, Rate) VALUES (?, ?, ?)",
                (1, 1, 0.99)
            )
