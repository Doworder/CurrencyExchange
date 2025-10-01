from dataclasses import dataclass, field
from decimal import Decimal


@dataclass
class GetCurrencyDTO:
    id: int
    code: str
    name: str
    sign: str


@dataclass
class GetRateDTO:
    id: int
    base_currency: GetCurrencyDTO
    target_currency: GetCurrencyDTO
    rate: Decimal


@dataclass
class GetExchangeDTO:
    base_currency: GetCurrencyDTO
    target_currency: GetCurrencyDTO
    rate: Decimal
    amount:Decimal
    converted_amount: Decimal = field(init=False)

    def __post_init__(self) -> None:
        self.converted_amount = self.rate * self.amount
