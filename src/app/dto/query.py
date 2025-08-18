from dataclasses import dataclass
from decimal import Decimal

from app.dto.validation_functions import (
    is_valid_currency_code,
    validate_currencies,
    validate_exchange_rate
)


@dataclass
class QueryCurrencyDTO:
    currency_code: str

    def __post_init__(self) -> None:
        is_valid_currency_code(self.currency_code)


@dataclass
class QueryRateDTO:
    base_currency: str
    target_currency: str

    def __post_init__(self) -> None:
        validate_currencies(self.base_currency, self.target_currency)


@dataclass
class QueryExchangeDTO:
    base_currency: str
    target_currency: str
    amount: Decimal

    def __post_init__(self) -> None:
        validate_currencies(self.base_currency, self.target_currency)
        validate_exchange_rate(self.amount)
