"""The shop's HTTP API."""
import json
import logging
from http.server import BaseHTTPRequestHandler, HTTPServer

from . import accounts, monitoring, orders, support
from .db import create

log = logging.getLogger(__name__)

ROUTES = {
    "/signup": lambda body: {"id": accounts.sign_up(**body)},
    "/close-account": lambda body: accounts.close_account(body["customer_id"]) or {"closed": True},
    "/orders": lambda body: {"id": orders.place_order(**body)},
    "/support": lambda body: {"id": support.open_ticket(**body)},
}


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        route = ROUTES.get(self.path)
        if route is None:
            self.send_error(404)
            return
        body = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}")
        try:
            result, status = route(body), 200
        except orders.AllergyConflict as conflict:
            result, status = {"error": f"Contains {conflict}"}, 409
        except Exception:
            # Logged as an error with its traceback, which Sentry receives as an issue.
            log.exception("Request to %s failed", self.path)
            result, status = {"error": "Something went wrong"}, 500
        payload = json.dumps(result).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(payload)


def main():
    monitoring.start()
    create()
    HTTPServer(("127.0.0.1", 8000), Handler).serve_forever()


if __name__ == "__main__":
    main()
