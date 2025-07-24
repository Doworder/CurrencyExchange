from abc import ABC, abstractmethod


class DatabaseManager(ABC):
    @abstractmethod
    def add_currency(self): ...

    @abstractmethod
    def add_rate(self): ...

    @abstractmethod
    def get_currency(self): ...

    @abstractmethod
    def get_rate(self): ...

    @abstractmethod
    def update_currency(self): ...

    @abstractmethod
    def update_rate(self): ...