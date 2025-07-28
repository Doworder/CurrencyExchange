import sqlite3
from pathlib import Path
from sqlite3 import OperationalError

connection = sqlite3.connect(Path("data/currency.db"))
cursor = connection.cursor()
try:
    cursor.execute('''
                CREATE TABLE Currencies(
                    ID INTEGER PRIMARY KEY AUTOINCREMENT, 
                  Code VARCHAR(3) NOT NULL UNIQUE, 
              FullName VARCHAR(100), 
                  Sign VARCHAR(5)
                  )
    ''')
    cursor.execute('''
                CREATE UNIQUE INDEX idx_currencies_code 
                       ON Currencies(Code)
    ''')
    cursor.execute('''
                CREATE TABLE ExchangeRates(
                    ID INTEGER PRIMARY KEY AUTOINCREMENT, 
        BaseCurrencyId INT NOT NULL, 
      TargetCurrencyId INT NOT NULL, 
                  Rate NUMERIC(6) NOT NULL, 
                       FOREIGN KEY (BaseCurrencyId)  REFERENCES Currencies (ID), 
                       FOREIGN KEY (TargetCurrencyId)  REFERENCES Currencies (ID)
                  )
    ''')
    cursor.execute('''
                CREATE UNIQUE INDEX idx_exchange_rates_pair 
                       ON ExchangeRates(BaseCurrencyId, TargetCurrencyId)
    ''')
except OperationalError as e:
    print(e)
finally:
    cursor.execute("SELECT * FROM sqlite_master WHERE type='table';")
print(cursor.fetchall())
connection.close()
