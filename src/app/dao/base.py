from abc import ABC, abstractmethod


class DatabaseManager(ABC):
    @abstractmethod
    def add_currency(self, entity): ...

    @abstractmethod
    def add_rate(self, entity): ...

    @abstractmethod
    def get_currency(self, entity): ...

    @abstractmethod
    def get_rate(self, entity): ...

    @abstractmethod
    def update_currency(self, entity): ...

    @abstractmethod
    def update_rate(self, entity): ...