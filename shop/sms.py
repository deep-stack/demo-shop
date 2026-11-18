"""Text messages sent through the SMS service."""
from .outside import post

SMS_URL = "https://sms.example.com/messages"


def send_order_reminder(phone, order_id):
    """Text the customer that their order is ready to collect."""
    post(SMS_URL, {"to": phone, "text": f"Order {order_id} is ready to collect."})
