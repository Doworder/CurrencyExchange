from dataclasses import dataclass
from decimal import Decimal


@dataclass
class QueryCurrencyDTO:
    currency_code: str


@dataclass
class QueryRateDTO:
    base_currency: str
    target_currency: str


@dataclass
class QueryExchangeDTO:
    base_currency: str
    target_currency: str
    amount: Decimal
