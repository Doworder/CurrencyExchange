class CurrencyValidationError(ValueError):
    """Базовое исключение для ошибок валидации валют"""
    pass

class InvalidCurrencyCodeError(CurrencyValidationError):
    """Некорректный код валюты"""
    pass

class InvalidExchangeRateError(CurrencyValidationError):
    """Некорректное значение курса"""
    pass

class SameCurrencyError(CurrencyValidationError):
    """Одинаковые валюты в паре"""
    pass