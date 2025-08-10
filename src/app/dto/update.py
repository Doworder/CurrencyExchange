from dataclasses import dataclass
from decimal import Decimal


@dataclass
class UpdateRateDTO:
    base_currency: str
    target_currency: str
    rate: Decimal