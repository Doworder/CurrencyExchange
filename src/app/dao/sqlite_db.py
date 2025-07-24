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

