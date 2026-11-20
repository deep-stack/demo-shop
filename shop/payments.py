"""Payments Stripe tells the shop about, through its webhook."""
import logging
import os

import stripe

from .db import connect

log = logging.getLogger(__name__)
stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")


def handle(payload, signature):
    """Check the event came from Stripe, then act on it."""
    event = stripe.Webhook.construct_event(payload, signature, os.environ["STRIPE_WEBHOOK_SECRET"])
    kind, item = event["type"], event["data"]["object"]
    if kind == "checkout.session.completed":
        # The order is paid: mark it so, and the kitchen starts on it.
        order_id = (item.get("metadata") or {}).get("order_id")
        if order_id:
            with connect() as conn:
                conn.execute("UPDATE orders SET status = 'paid' WHERE id = %s", (order_id,))
        log.info("Checkout %s completed", item["id"])
    elif kind == "invoice.paid":
        # A membership renewed.
        log.info("Membership %s renewed", item["subscription"])
    elif kind == "customer.subscription.deleted":
        log.info("Membership %s cancelled", item["id"])
    return {"received": True}
