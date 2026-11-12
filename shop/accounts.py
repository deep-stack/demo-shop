"""Customer accounts: signing up and closing an account."""
from datetime import datetime, timezone

from . import analytics, mailer
from .db import connect


def sign_up(email, full_name, phone, allergies, street, city, postcode):
    """Create a customer and their address, then tell analytics about the new signup."""
    now = datetime.now(timezone.utc).isoformat()
    with connect() as conn:
        customer_id = conn.execute(
            "INSERT INTO customers (email, full_name, phone, allergies, created_at) VALUES (%s, %s, %s, %s, %s) "
            "RETURNING id", (email, full_name, phone, allergies, now)).fetchone()["id"]
        conn.execute("INSERT INTO addresses (customer_id, street, city, postcode) VALUES (%s, %s, %s, %s)",
                     (customer_id, street, city, postcode))
    analytics.track_signup(email, city)
    return customer_id


def close_account(customer_id):
    """Close an account: delete the customer and their addresses, and keep payments for the accounts
    with the card number removed."""
    with connect() as conn:
        email = conn.execute("SELECT email FROM customers WHERE id = %s", (customer_id,)).fetchone()["email"]
        conn.execute("DELETE FROM addresses WHERE customer_id = %s", (customer_id,))
        conn.execute("UPDATE payments SET card_last4 = NULL, customer_id = NULL WHERE customer_id = %s",
                     (customer_id,))
        conn.execute("UPDATE orders SET customer_id = NULL WHERE customer_id = %s", (customer_id,))
        conn.execute("DELETE FROM support_tickets WHERE customer_email = %s", (email,))
        conn.execute("DELETE FROM customers WHERE id = %s", (customer_id,))
    mailer.send_goodbye(email)
