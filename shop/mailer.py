"""Emails sent through the mail service."""
import os

from .outside import post

MAIL_URL = os.environ.get("MAIL_URL", "https://mail.example.com/v1/send")


def send_receipt(email, full_name, order_id, total):
    """Email the customer a receipt for their order."""
    post(MAIL_URL, {"to": email, "name": full_name,
                    "subject": f"Your order {order_id}", "body": f"Thank you! Total: {total / 100:.2f}"})


def send_goodbye(email):
    """Confirm to the customer that their account is closed."""
    post(MAIL_URL, {"to": email, "subject": "Your account is closed", "body": "We have removed your details."})
