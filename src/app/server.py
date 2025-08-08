import json
import logging
import sqlite3
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs

from app.dao import SQLiteManager, DatabaseManager
from app.dto import AddCurrencyDTO, AddRateDTO


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class CurrencyHandler(BaseHTTPRequestHandler):
    db_manager: DatabaseManager

    def set_db_manager(self, db_manager: DatabaseManager) -> None:
        self.db_manager = db_manager

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"GET method called.")

    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"POST method called.")
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
                    self._send_success_response()

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
                        rate=float(query_data.get("rate")[0])
                    )
                except TypeError as e:
                    logger.debug(f'Type error: {e.args}')
                    self._send_missing_field_error("rate")
                    return

                try:
                    self._add_rate(new_rate)
                    self._send_success_response()

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

    def do_PATCH(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"PATCH method called.")

    def _add_currency(self, entity):
        self.db_manager.add_currency(entity)

    def _add_rate(self, entity):
        self.db_manager.add_rate(entity)

    def _send_success_response_get(self, data=None):
        self._send_response(200, data=data)

    def _send_success_response_post(self):
        self._send_response(201)

    def _send_missing_field_error(self, field_name):
        message = f'Missing required field: {field_name}'
        self._send_response(400, message)

    def _send_rate_not_found_error(self):
        message = 'The currency pair does not exist in the database'
        self._send_response(404, message)

    def _send_conflict_error(self, currency_code):
        message = f'Currency with code {currency_code} already exists'
        self._send_response(409, message)

    def _send_conflict_rate_error(self):
        message = f'A currency pair with this code already exists.'
        self._send_response(409, message)

    def _send_server_error(self, error_message=None, error_details=None):
        if error_message:
            error_message = 'An unexpected error occurred'
        else:
            error_message = error_message + ': ' + error_details

        self._send_response(500, error_message)

    def _send_response(self, status_code: int, message=None, data=None):
        self.send_response(status_code, message)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))


def main() :
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