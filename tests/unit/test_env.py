"""Settings read from a .env file."""
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from shop.monitoring import load_env


class EnvTests(unittest.TestCase):
    def test_values_in_env_are_read_and_quotes_removed(self):
        with tempfile.TemporaryDirectory() as folder, mock.patch.dict(os.environ, {}, clear=True):
            path = Path(folder, ".env")
            path.write_text("# a comment\nSHOP_NAME='Corner shop'\nEMPTY=\n")
            load_env(path)
            self.assertEqual(os.environ["SHOP_NAME"], "Corner shop")

    def test_what_is_already_set_is_kept(self):
        with tempfile.TemporaryDirectory() as folder, mock.patch.dict(os.environ, {"SHOP_NAME": "kept"}, clear=True):
            path = Path(folder, ".env")
            path.write_text("SHOP_NAME=other\n")
            load_env(path)
            self.assertEqual(os.environ["SHOP_NAME"], "kept")


if __name__ == "__main__":
    unittest.main()
