"""Closing an account removes what the shop keeps about the customer."""
import unittest
from unittest import mock

from shop import accounts


class Recorder:
    """A stand-in for the database that records each statement."""

    def __init__(self):
        self.statements = []

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    def execute(self, sql, params=()):
        self.statements.append(" ".join(sql.split()))
        return mock.Mock(fetchone=lambda: {"email": "ana@example.com"})


class CloseAccountTests(unittest.TestCase):
    def test_closing_an_account_removes_the_customers_support_tickets(self):
        db = Recorder()
        with mock.patch.object(accounts, "connect", return_value=db), \
                mock.patch.object(accounts.mailer, "send_goodbye"):
            accounts.close_account(7)
        touched = [sql for sql in db.statements if "support_tickets" in sql]
        self.assertTrue(touched, "close_account left the customer's support tickets in place")


if __name__ == "__main__":
    unittest.main()
