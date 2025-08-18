from decimal import Decimal

from app.exceptions.validation import (
    InvalidCurrencyCodeError,
    SameCurrencyError,
    InvalidExchangeRateError
)

VALID_ISO_CURRENCIES = {
    "AED", "AFN", "ALL", "AMD", "ANG", "AOA", "ARS", "AUD", "AWG", "AZN",
    "BAM", "BBD", "BDT", "BGN", "BHD", "BIF", "BMD", "BND", "BOB", "BOV",
    "BRL", "BSD", "BTN", "BWP", "BYN", "BYR", "BZD", "CAD", "CDF", "CHE",
    "CHF", "CHW", "CLF", "CLP", "CNY", "COP", "COU", "CRC", "CUC", "CUP",
    "CVE", "CZK", "DJF", "DKK", "DOP", "DZD", "EGP", "ERN", "ETB", "EUR",
    "FJD", "FKP", "GBP", "GEL", "GGP", "GHS", "GIP", "GMD", "GNF", "GTQ",
    "GYD", "HKD", "HNL", "HRK", "HTG", "HUF", "IDR", "ILS", "IMP", "INR",
    "IQD", "IRR", "ISK", "JEP", "JMD", "JOD", "JPY", "KES", "KGS", "KHR",
    "KMF", "KPW", "KRW", "KWD", "KYD", "KZT", "LAK", "LBP", "LKR", "LRD",
    "LSL", "LYD", "MAD", "MDL", "MGA", "MKD", "MMK", "MNT", "MOP", "MRO",
    "MRU", "MUR", "MVR", "MWK", "MXN", "MXV", "MYR", "MZN", "NAD", "NGN",
    "NIO", "NOK", "NPR", "NZD", "OMR", "PAB", "PEN", "PGK", "PHP", "PKR",
    "PLN", "PYG", "QAR", "RON", "RSD", "RUB", "RWF", "SAR", "SBD", "SCR",
    "SDG", "SEK", "SGD", "SHP", "SLE", "SLL", "SOS", "SPL", "SRD", "SSP",
    "STD", "STN", "SVC", "SYP", "SZL", "THB", "TJS", "TMT", "TND", "TOP",
    "VEF", "TRY", "TTD", "TVD", "TWD", "TZS", "UAH", "UGX", "USD", "USN",
    "UYI", "UYU", "UZS", "VES", "VND", "VUV", "WST", "XAF", "XCD", "XDR",
    "XOF", "XPF", "XSU", "XUA", "YER", "ZAR", "ZMW", "ZWD", "ZWL"
}

def validate_currencies(base_currency: str, target_currency: str) -> None:
    """Проверка формата валютных пар"""
    for currency in (base_currency, target_currency):
        if not is_valid_currency_code(currency):
            raise InvalidCurrencyCodeError(
                f"Invalid currency code: {currency}. "
                "Must be 3 uppercase letters."
            )

    if base_currency == target_currency:
        raise SameCurrencyError(
            "Currencies must be different: "
            f"{base_currency}/{target_currency}"
        )

def validate_exchange_rate(amount: Decimal) -> None:
    """Проверка корректности курса"""
    if not isinstance(amount, Decimal):
        raise InvalidExchangeRateError(
            f"Exchange rate must be numeric. Got: {type(amount)}"
        )

    if amount <= 0:
        raise InvalidExchangeRateError(
            f"Exchange rate must be positive. Got: {amount}"
        )

def is_valid_currency_code(currency: str) -> bool:
    """Проверяет формат кода валюты"""
    return (
            isinstance(currency, str)
            and len(currency) == 3
            and currency in VALID_ISO_CURRENCIES
            and currency.isalpha()
            and currency.isupper()
    )


