"""The shop served over HTTP, as a customer reaches it. Slow on purpose, as a browser test is."""
import random
import threading
import time
import unittest
import urllib.error
import urllib.request
from http.server import HTTPServer

from shop.server import Handler


class CheckoutTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = HTTPServer(("127.0.0.1", 0), Handler)
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()
        cls.base = f"http://127.0.0.1:{cls.server.server_port}"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()

    def get(self, path):
        try:
            with urllib.request.urlopen(self.base + path, timeout=10) as response:
                return response.status
        except urllib.error.HTTPError as error:
            return error.code

    def test_an_unknown_page_is_not_found(self):
        time.sleep(4)  # a browser test waits for the page to load
        self.assertEqual(self.get("/no-such-page"), 404)

    def test_the_shop_answers_quickly(self):
        # Flaky on purpose: it times a single request against a tight limit, so a busy runner fails it.
        started = time.monotonic()
        self.get("/no-such-page")
        time.sleep(6)
        took = time.monotonic() - started
        self.assertLess(took + random.uniform(0, 1), 6.7, "the shop answered too slowly")


if __name__ == "__main__":
    unittest.main()
