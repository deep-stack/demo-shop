"""Support tickets customers open from the contact form."""
from datetime import datetime, timezone

from .db import connect


def open_ticket(customer_email, message):
    """Keep a customer's question for the support team. Tickets are never removed."""
    with connect() as conn:
        return conn.execute("INSERT INTO support_tickets (customer_email, message, created_at) VALUES (?, ?, ?)",
                            (customer_email, message, datetime.now(timezone.utc).isoformat())).lastrowid
