from dataclasses import dataclass


@dataclass
class AddCurrencyDTO:
    currency_code: str
    full_name: str
    sign: str


@dataclass
class AddRateDTO:
    base_currency: str
    target_currency: str
    rate: float
