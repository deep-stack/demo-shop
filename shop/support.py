"""Support tickets customers open from the contact form."""
from datetime import datetime, timezone

from .db import connect
from .outside import post

HELPDESK_URL = "https://helpdesk.example.com/tickets"


def open_ticket(customer_email, message):
    """Keep a customer's question for the support team, and copy it to the helpdesk service. Tickets are never removed."""
    with connect() as conn:
        ticket = conn.execute("INSERT INTO support_tickets (customer_email, message, created_at) VALUES (?, ?, ?)",
                              (customer_email, message, datetime.now(timezone.utc).isoformat())).lastrowid
    post(HELPDESK_URL, {"requester": customer_email, "body": message, "ticket": ticket})
    return ticket
