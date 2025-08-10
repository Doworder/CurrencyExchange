from dataclasses import dataclass
from decimal import Decimal


@dataclass
class GetCurrencyDTO:
    id: int
    currency_code: str
    full_name: str
    sign: str


@dataclass
class GetRateDTO:
    id: int
    base_currency: str
    target_currency: str
    rate: Decimal
