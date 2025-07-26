from dataclasses import dataclass


@dataclass
class CurrencyAddDTO:
    currency_code: str
    full_name: str
    sign: str


@dataclass
class RateAddDTO:
    base_currency: str
    target_currency: str
    rate: float
