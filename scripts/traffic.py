"""Send the shop a few requests that fail, so Sentry has real errors to show. Start the shop first."""
import json
import urllib.error
import urllib.request

SHOP = "http://127.0.0.1:8000"

REQUESTS = [
    # Signs up, then fails telling analytics: the customer is saved, the request still fails.
    ("/signup", {"email": "ana@team.example", "full_name": "Ana Silva", "phone": "+15550100", "allergies": "peanuts",
                 "street": "1 Main St", "city": "Springfield", "postcode": "12345"}),
    # An order for a customer who does not exist.
    ("/orders", {"customer_id": 999999, "total": 1250, "contains": ["milk"], "card_last4": "4242"}),
    # A support ticket, which fails copying it to the helpdesk.
    ("/support", {"customer_email": "ana@team.example", "message": "My order arrived damaged"}),
    # Closing an account that does not exist.
    ("/close-account", {"customer_id": 999999}),
    # A sign-up missing its fields.
    ("/signup", {"email": "ben@team.example"}),
]


def send(path, body):
    request = urllib.request.Request(SHOP + path, data=json.dumps(body).encode(),
                                     headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return response.status
    except urllib.error.HTTPError as error:
        return error.code


if __name__ == "__main__":
    for path, body in REQUESTS:
        print(path, send(path, body))
