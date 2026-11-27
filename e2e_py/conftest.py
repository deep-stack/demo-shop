"""The shop front, served for the browser tests."""

import subprocess
import sys
import time
from pathlib import Path
from urllib.request import urlopen

import pytest

WEB = Path(__file__).resolve().parent.parent / "web"
PORT = 4174


@pytest.fixture(scope="session")
def base_url():
    server = subprocess.Popen(
        [sys.executable, "-m", "http.server", str(PORT), "--bind", "127.0.0.1", "-d", str(WEB)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    url = f"http://127.0.0.1:{PORT}"
    for _ in range(50):
        try:
            urlopen(url + "/index.html")
            break
        except OSError:
            time.sleep(0.1)
    yield url
    server.terminate()
