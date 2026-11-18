"""Send the shop a few sample requests. Start the shop first, or give the address it is deployed at:
python scripts/traffic.py https://shop.example.test"""
import json
import sys
import time
import urllib.error
import urllib.request

SHOP = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else "http://127.0.0.1:8000"
# On Vercel each route is a function under /api.
PREFIX = "/api" if len(sys.argv) > 1 else ""
# A new customer each run, as emails are unique.
EMAIL = f"ana+{int(time.time())}@team.example"

REQUESTS = [
    # A new customer signs up.
    ("/signup", {"email": EMAIL, "full_name": "Ana Silva", "phone": "+15550100", "allergies": "peanuts",
                 "street": "1 Main St", "city": "Springfield", "postcode": "12345"}),
    # An order.
    ("/orders", {"customer_id": 1, "total": 1250, "contains": ["milk"], "card_last4": "4242"}),
    # An order for a customer who does not exist.
    ("/orders", {"customer_id": 999999, "total": 1250, "contains": ["milk"], "card_last4": "4242"}),
    # A support ticket.
    ("/support", {"customer_email": EMAIL, "message": "My order arrived damaged"}),
    # Closing an account that does not exist.
    ("/close-account", {"customer_id": 999999}),
    # A sign-up missing its fields.
    ("/signup", {"email": "ben@team.example"}),
]


def send(path, body):
    request = urllib.request.Request(SHOP + PREFIX + path, data=json.dumps(body).encode(),
                                     headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return response.status
    except urllib.error.HTTPError as error:
        return error.code


if __name__ == "__main__":
    for path, body in REQUESTS:
        print(path, send(path, body))
