"""The shop's HTTP API."""
import json
import logging
from http.server import BaseHTTPRequestHandler, HTTPServer

from . import accounts, monitoring, orders, payments, reports, support
from .db import create

log = logging.getLogger(__name__)

ROUTES = {
    "/signup": lambda body: {"id": accounts.sign_up(**body)},
    "/close-account": lambda body: accounts.close_account(body["customer_id"]) or {"closed": True},
    "/orders": lambda body: {"id": orders.place_order(**body)},
    "/support": lambda body: {"id": support.open_ticket(**body)},
}
# Jobs a scheduler calls with GET, such as Vercel's cron jobs.
JOBS = {
    "/nightly-report": lambda: reports.send_nightly_report(),
}


def route_of(path):
    """The shop's route for a request path: on Vercel each route is a function under /api."""
    path = path.split("?")[0]
    return path.removeprefix("/api") if path.startswith("/api/") else path


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        job = JOBS.get(route_of(self.path))
        if job is None:
            self.send_error(404)
            return
        self.answer(lambda: job())

    def do_POST(self):
        if route_of(self.path) == "/stripe-webhook":
            # Stripe signs the body as it sent it, so it is checked before it is read.
            payload = self.rfile.read(int(self.headers.get("Content-Length", 0)))
            self.answer(lambda: payments.handle(payload, self.headers.get("Stripe-Signature")))
            return
        route = ROUTES.get(route_of(self.path))
        if route is None:
            self.send_error(404)
            return
        body = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}")
        self.answer(lambda: route(body))

    def answer(self, work):
        try:
            result, status = work(), 200
        except orders.AllergyConflict as conflict:
            result, status = {"error": f"Contains {conflict}"}, 409
        except Exception:
            # Logged as an error with its traceback.
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
