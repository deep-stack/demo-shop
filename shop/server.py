"""The shop's HTTP API."""
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

from . import accounts, orders, support
from .db import create

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
        payload = json.dumps(result).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(payload)


def main():
    create()
    HTTPServer(("127.0.0.1", 8000), Handler).serve_forever()


if __name__ == "__main__":
    main()
