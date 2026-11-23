"""The shop's front door, served over HTTP as a customer's browser reaches it."""
import threading
import unittest
import urllib.error
import urllib.request
from http.server import HTTPServer

from shop.server import Handler


class StorefrontTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = HTTPServer(("127.0.0.1", 0), Handler)
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()
        cls.base = f"http://127.0.0.1:{cls.server.server_port}"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()

    def test_a_missing_page_says_so(self):
        try:
            urllib.request.urlopen(self.base + "/missing", timeout=10)
            status = 200
        except urllib.error.HTTPError as error:
            status = error.code
        self.assertEqual(status, 404)


if __name__ == "__main__":
    unittest.main()
