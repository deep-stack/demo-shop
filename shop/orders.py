"""Placing an order and paying for it."""
from . import mailer, sms
from .db import connect


class AllergyConflict(Exception):
    pass


def place_order(customer_id, total, contains, card_last4):
    """Check the order against the customer's allergies, record the order and payment, and email a receipt."""
    with connect() as conn:
        customer = conn.execute("SELECT email, full_name, phone, allergies FROM customers WHERE id = ?",
                                (customer_id,)).fetchone()
        allergies = {item.strip() for item in (customer["allergies"] or "").split(",") if item.strip()}
        if allergies & set(contains):
            raise AllergyConflict(", ".join(sorted(allergies & set(contains))))
        order_id = conn.execute("INSERT INTO orders (customer_id, total) VALUES (?, ?)",
                                (customer_id, total)).lastrowid
        conn.execute("INSERT INTO payments (customer_id, card_last4, amount) VALUES (?, ?, ?)",
                     (customer_id, card_last4, total))
    mailer.send_receipt(customer["email"], customer["full_name"], order_id, total)
    if customer["phone"]:
        sms.send_order_reminder(customer["phone"], order_id)
    return order_id
