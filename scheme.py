import sqlite3
from pathlib import Path
from sqlite3 import OperationalError

connection = sqlite3.connect(Path("data/currency.db"))
cursor = connection.cursor()
try:
    cursor.execute('''
                CREATE TABLE Currencies(
                    ID INTEGER PRIMARY KEY AUTOINCREMENT, 
                  Code VARCHAR(3) UNIQUE, 
              FullName VARCHAR, 
                  Sign VARCHAR
                  )
    ''')
    cursor.execute('''
                CREATE TABLE ExchangeRates(
                    ID INTEGER PRIMARY KEY AUTOINCREMENT, 
        BaseCurrencyId INT UNIQUE, 
      TargetCurrencyId INT UNIQUE, 
                  Rate NUMERIC(6), 
                       FOREIGN KEY (ID)  REFERENCES Currencies (ID), 
                       FOREIGN KEY (ID)  REFERENCES Currencies (ID)
                  )
    ''')
except OperationalError as e:
    print(e)
finally:
    cursor.execute("SELECT * FROM sqlite_master WHERE type='table';")
print(cursor.fetchall())
connection.close()
