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
    baseCurrency: GetCurrencyDTO
    targetCurrency: GetCurrencyDTO
    rate: Decimal


@dataclass
class GetExchangeDTO:
    baseCurrency: GetCurrencyDTO
    targetCurrency: GetCurrencyDTO
    rate: Decimal
    amount:Decimal
    convertedAmount: Decimal = field(init=False)

    def __post_init__(self) -> None:
        self.convertedAmount = self.rate * self.amount
