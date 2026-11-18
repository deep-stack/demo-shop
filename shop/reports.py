"""The nightly report for the marketing team, which a scheduler runs once a day."""
from .analytics import ANALYTICS_URL
from .db import connect
from .outside import post


def send_nightly_report():
    """Count yesterday's signups and orders, and send them to the analytics service."""
    with connect() as conn:
        found = conn.execute(
            "SELECT (SELECT count(*) FROM customers WHERE created_at >= now() - interval '1 day') AS signups, "
            "(SELECT count(*) FROM orders WHERE created_at >= now() - interval '1 day') AS orders").fetchone()
    post(ANALYTICS_URL, {"event": "nightly-report", **found})
    return found
