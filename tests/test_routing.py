"""Paths the shop's server maps to its routes."""
import unittest

from shop.server import route_of


class RoutingTests(unittest.TestCase):
    def test_a_query_is_not_part_of_the_route(self):
        self.assertEqual(route_of("/orders?page=2"), "/orders")

    def test_only_the_api_prefix_is_removed(self):
        self.assertEqual(route_of("/apiary"), "/apiary")


if __name__ == "__main__":
    unittest.main()
