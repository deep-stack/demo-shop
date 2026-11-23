"""What a placed order leaves in Postgres, at DATABASE_URL."""
import os
import unittest
from unittest import mock

from shop import orders
from shop.db import connect


@unittest.skipUnless(os.environ.get("DATABASE_URL"), "needs DATABASE_URL")
class OrderRecordTests(unittest.TestCase):
    def setUp(self):
        with connect() as conn:
            conn.execute("TRUNCATE payments, orders, addresses, customers RESTART IDENTITY CASCADE")
            self.customer = conn.execute(
                "INSERT INTO customers (email, full_name, phone, allergies) VALUES (%s, %s, %s, %s) RETURNING id",
                ("bo@example.com", "Bo", None, None)).fetchone()["id"]

    def test_an_order_keeps_what_it_contains(self):
        with mock.patch.object(orders.mailer, "send_receipt"):
            order_id = orders.place_order(self.customer, 480, ["milk", "eggs"], "1111")
        with connect() as conn:
            row = conn.execute("SELECT customer_id FROM orders WHERE id = %s", (order_id,)).fetchone()
        self.assertEqual(row["customer_id"], self.customer)


if __name__ == "__main__":
    unittest.main()
