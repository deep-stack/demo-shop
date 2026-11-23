"""Emails the shop sends, checked without reaching the mail service."""
import unittest
from unittest import mock

from shop import mailer


class MailerTests(unittest.TestCase):
    def test_a_receipt_shows_the_total_in_pounds(self):
        with mock.patch.object(mailer, "post") as post:
            mailer.send_receipt("ann@example.com", "Ann", 7, 1250)
        payload = post.call_args.args[1]
        self.assertEqual(payload["subject"], "Your order 7")
        self.assertIn("12.50", payload["body"])

    def test_a_goodbye_goes_to_the_customer(self):
        with mock.patch.object(mailer, "post") as post:
            mailer.send_goodbye("ann@example.com")
        self.assertEqual(post.call_args.args[1]["to"], "ann@example.com")


if __name__ == "__main__":
    unittest.main()
