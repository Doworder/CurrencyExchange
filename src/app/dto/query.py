from dataclasses import dataclass


@dataclass
class QueryCurrencyDTO:
    currency_code: str


@dataclass
class QueryRateDTO:
    base_currency: str
    target_currency: str
