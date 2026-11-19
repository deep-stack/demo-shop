"""Emails sent through Resend."""
import os

import resend

resend.api_key = os.environ.get("RESEND_API_KEY")


def send_receipt(email, full_name, order_id, total):
    """Email the customer a receipt for their order."""
    resend.Emails.send({
        "from": "Shop <onboarding@resend.dev>",
        "to": [email],
        "subject": f"Your order {order_id}",
        "html": f"<p>Thank you, {full_name}! Total: {total / 100:.2f}</p>",
    })


def send_goodbye(email):
    """Confirm to the customer that their account is closed."""
    resend.Emails.send({
        "from": os.environ["EMAIL_FROM"],
        "to": [email],
        "subject": "Your account is closed",
        "html": "<p>We have removed your details.</p>",
    })
