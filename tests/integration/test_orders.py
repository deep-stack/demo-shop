"""Orders placed against a real Postgres database, at DATABASE_URL."""
import os
import unittest
from unittest import mock

from shop import orders
from shop.db import connect


@unittest.skipUnless(os.environ.get("DATABASE_URL"), "needs DATABASE_URL")
class OrderTests(unittest.TestCase):
    def setUp(self):
        with connect() as conn:
            conn.execute("TRUNCATE payments, orders, addresses, customers RESTART IDENTITY CASCADE")
            self.customer = conn.execute(
                "INSERT INTO customers (email, full_name, phone, allergies) VALUES (%s, %s, %s, %s) RETURNING id",
                ("ann@example.com", "Ann", None, "peanuts, milk")).fetchone()["id"]

    def test_an_order_is_recorded_with_its_payment(self):
        with mock.patch.object(orders.mailer, "send_receipt") as receipt:
            order_id = orders.place_order(self.customer, 1250, ["bread"], "4242")
        with connect() as conn:
            self.assertEqual(conn.execute("SELECT total FROM orders WHERE id = %s", (order_id,)).fetchone()["total"], 1250)
            self.assertEqual(conn.execute("SELECT count(*) AS n FROM payments").fetchone()["n"], 1)
        receipt.assert_called_once()

    def test_an_order_with_an_allergen_is_refused_and_not_recorded(self):
        with self.assertRaises(orders.AllergyConflict):
            orders.place_order(self.customer, 900, ["milk", "flour"], "4242")
        with connect() as conn:
            self.assertEqual(conn.execute("SELECT count(*) AS n FROM orders").fetchone()["n"], 0)


if __name__ == "__main__":
    unittest.main()
