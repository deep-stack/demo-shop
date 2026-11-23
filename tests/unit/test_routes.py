"""Requests reach the shop's routes, served locally or as Vercel functions under /api."""
import unittest

from shop.server import route_of


class RouteTests(unittest.TestCase):
    def test_a_route_is_the_same_with_or_without_the_api_prefix(self):
        self.assertEqual(route_of("/orders"), "/orders")
        self.assertEqual(route_of("/api/orders"), "/orders")
        self.assertEqual(route_of("/api/nightly-report?x=1"), "/nightly-report")
        self.assertEqual(route_of("/api/stripe-webhook"), "/stripe-webhook")


if __name__ == "__main__":
    unittest.main()
