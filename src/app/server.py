import json
import logging
import sqlite3
from dataclasses import asdict
from decimal import Decimal
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any, TypeAlias
from urllib.parse import parse_qs

from app.dao import SQLiteManager, DatabaseManager
from app.dto import (
    AddCurrencyDTO,
    AddRateDTO,
    QueryCurrencyDTO,
    QueryRateDTO, UpdateRateDTO,
)

ResponseData: TypeAlias = list[dict[str, Any]] | dict[str, Any] | None

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class CurrencyHandler(BaseHTTPRequestHandler):
    db_manager: DatabaseManager

    def set_db_manager(self, db_manager: DatabaseManager) -> None:
        self.db_manager = db_manager

    def do_GET(self) -> None:
        path_part = self.path.split('/')
        logger.debug(f"Parted path: {path_part}")
        match path_part[-1]:
            case "currencies":
                currency_list = self._get_all_currency()
                self._send_success_response_get(data=currency_list)

            case s if len(s) == 3 and path_part[-2] == "currency":
                try:
                    currency_data = self._get_currency(QueryCurrencyDTO(s))
                    self._send_success_response_get(data=currency_data)

                except ValueError:
                    self.send_error(404)

            case "exchangeRate":
                self.send_error(400, message="The currency codes of the pair are missing in the address")

            case r if not len(r):
                self.send_error(400, message="The currency codes of the pair are missing in the address")

            case "exchangeRates":
                rate_list = self._get_all_rate()
                self._send_success_response_get(data=rate_list)

            case r if len(r) == 6 and path_part[-2] == "exchangeRate":
                try:
                    base_currency = r[:3]
                    target_currency = r[3:]
                    rate_data = self._get_rate(QueryRateDTO(base_currency, target_currency))
                    self._send_success_response_get(data=rate_data)

                except ValueError:
                    self.send_error(404)

            case _:
                self.send_error(404)

    def do_POST(self) -> None:
        content_type = self.headers.get("Content-Type", "")
        if content_type != "application/x-www-form-urlencoded":
            self.send_error(400, "Content-Type must be application/x-www-form-urlencoded")
            return

        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length)
        query_data: dict[str, list[str]] = parse_qs(post_data.decode("utf-8"))
        logger.debug(f'Query data: {query_data}')

        path_part = self.path.split('/')
        match path_part[-1]:
            case "currencies":
                new_currency = AddCurrencyDTO(
                    currency_code=query_data.get("code")[0],
                    full_name=query_data.get("name")[0],
                    sign=query_data.get("sign")[0]
                )
                logger.debug(f'New currency DTO created: {new_currency}')
                try:
                    self._add_currency(new_currency)
                    currency_data = self._get_currency(QueryCurrencyDTO(currency_code=new_currency.currency_code))
                    self._send_success_response_post(currency_data)

                except sqlite3.IntegrityError:
                    self._send_conflict_error(new_currency.currency_code)

                except sqlite3.OperationalError as e:
                    logger.debug(f'Server error: {e.sqlite_errorcode}, {e.sqlite_errorname}')
                    self._send_server_error()

            case "exchangeRates":
                try:
                    new_rate = AddRateDTO(
                        base_currency=query_data.get("baseCurrencyCode")[0],
                        target_currency=query_data.get("targetCurrencyCode")[0],
                        rate=Decimal(query_data.get("rate")[0])
                    )
                except TypeError as e:
                    logger.debug(f'Type error: {e.args}')
                    self._send_missing_field_error("rate")
                    return

                try:
                    self._add_rate(new_rate)
                    rate_data = self._get_rate(QueryRateDTO(
                        base_currency=new_rate.base_currency,
                        target_currency=new_rate.target_currency
                    ))
                    self._send_success_response_post(rate_data)

                except sqlite3.IntegrityError as e:
                    logger.debug(f'Returned error: {e.sqlite_errorname}')
                    logger.debug(f'Returned error code: {e.sqlite_errorcode}')
                    match e.sqlite_errorcode:
                        case 1299:
                            self._send_rate_not_found_error()

                        case 2067:
                            self._send_conflict_rate_error()

                        case _:
                            self._send_server_error()

            case _:
                self.send_error(404)

    def do_PATCH(self) -> None:
        content_type = self.headers.get("Content-Type", "")
        if content_type != "application/x-www-form-urlencoded":
            self.send_error(400, "Content-Type must be application/x-www-form-urlencoded")
            return

        content_length = int(self.headers.get("Content-Length", 0))
        patch_data = self.rfile.read(content_length)
        query_data: dict[str, list[str]] = parse_qs(patch_data.decode("utf-8"))
        logger.debug(f'Query data: {query_data}')

        path_part = self.path.split('/')
        logger.debug(f"Parted path: {path_part}")
        match path_part[-1]:
            case r if len(r) == 6 and path_part[-2] == "exchangeRate":
                try:
                    base_currency = r[:3]
                    target_currency = r[3:]
                    new_rate_value = UpdateRateDTO(
                        base_currency=base_currency,
                        target_currency=target_currency,
                        rate=Decimal(query_data.get("rate")[0])
                    )
                    logger.debug(f"Rate decimal: {Decimal(query_data.get('rate')[0])}")
                    self._update_rate(new_rate_value)
                    rate_data = self._get_rate(QueryRateDTO(
                        base_currency=new_rate_value.base_currency,
                        target_currency=new_rate_value.target_currency
                    ))
                    self._send_success_response_get(rate_data)

                except ValueError:
                    self.send_error(404, message="The currency pair is missing from the database")

                # except sqlite3.ProgrammingError:
                #     self._send_server_error()

            case _:
                self.send_error(404)

    def _add_currency(self, entity: AddCurrencyDTO) -> None:
        self.db_manager.add_currency(entity)

    def _add_rate(self, entity: AddRateDTO) -> None:
        self.db_manager.add_rate(entity)

    def _get_currency(self, entity: QueryCurrencyDTO) -> dict[str, Any]:
        currency = self.db_manager.get_currency(entity)
        logger.debug(f'currency list: {currency}')
        if currency is None:
            raise ValueError("Currency not found")
        return asdict(currency)

    def _get_all_currency(self) -> list[dict[str, Any]]:
        currencies = self.db_manager.get_all_currency()
        logger.debug(f'currency list: {currencies}')
        return [asdict(item) for item in currencies]

    def _get_rate(self, entity: QueryRateDTO) -> dict[str, Any]:
        rate = self.db_manager.get_rate(entity)
        logger.debug(f'rate list: {rate}')
        if rate is None:
            raise ValueError("Currency not found")
        return asdict(rate)

    def _get_all_rate(self) -> list[dict[str, Any]]:
        rates = self.db_manager.get_all_rate()
        logger.debug(f'currency list: {rates}')
        return [asdict(item) for item in rates]

    def _update_rate(self, entity: UpdateRateDTO) -> None:
        self.db_manager.update_rate(entity)

    def _send_success_response_get(self, data: ResponseData=None) -> None:
        self._send_response(200, data=data)

    def _send_success_response_post(self, data: ResponseData=None) -> None:
        self._send_response(201, data=data)

    def _send_missing_field_error(self, field_name: str) -> None:
        message = f'Missing required field: {field_name}'
        self._send_response(400, message)

    def _send_rate_not_found_error(self) -> None:
        message = 'The currency pair does not exist in the database'
        self._send_response(404, message)

    def _send_conflict_error(self, currency_code: str) -> None:
        message = f'Currency with code {currency_code} already exists'
        self._send_response(409, message)

    def _send_conflict_rate_error(self) -> None:
        message = f'A currency pair with this code already exists.'
        self._send_response(409, message)

    def _send_server_error(self, error_message: str | None=None, error_details: str | None=None) -> None:
        if error_message is None:
            error_message = 'An unexpected error occurred'
        else:
            error_message = error_message + ': ' + error_details

        self._send_response(500, error_message)

    def _send_response(self, status_code: int, message: str | None=None, data: ResponseData=None) -> None:
        self.send_response(status_code, message)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))


def main() -> None :
    db = SQLiteManager(Path("data/currency.db"))
    server_address = ('', 8000)
    CurrencyHandler.db_manager = db
    server = HTTPServer(server_address, CurrencyHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()

if __name__ == '__main__':
    main()