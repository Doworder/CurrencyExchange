from abc import ABC, abstractmethod

from app.dto import (
    AddCurrencyDTO,
    AddRateDTO,
    GetCurrencyDTO,
    GetRateDTO,
    QueryCurrencyDTO,
    QueryRateDTO,
    UpdateRateDTO,
)


class DatabaseManager(ABC):
    @abstractmethod
    def add_currency(self, entity: AddCurrencyDTO) -> None: ...

    @abstractmethod
    def add_rate(self, entity:AddRateDTO) -> None: ...

    @abstractmethod
    def get_currency(self, entity: QueryCurrencyDTO) -> GetCurrencyDTO | None: ...

    @abstractmethod
    def get_all_currency(self) -> list[GetCurrencyDTO]: ...

    @abstractmethod
    def get_rate(self, entity: QueryRateDTO) -> GetRateDTO | None: ...

    @abstractmethod
    def get_all_rate(self) -> list[GetRateDTO]: ...

    @abstractmethod
    def update_rate(self, entity: UpdateRateDTO) -> None: ...
