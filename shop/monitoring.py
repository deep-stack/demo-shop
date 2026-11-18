"""Error reporting to Sentry, on when SENTRY_DSN is set in the environment or in .env."""
import logging
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
log = logging.getLogger(__name__)


def load_env(path=ROOT / ".env"):
    """Read NAME=value lines from .env into the environment, keeping what is already set."""
    if not path.is_file():
        return
    for line in path.read_text().splitlines():
        name, equals, value = line.strip().partition("=")
        if equals and name and not name.startswith("#"):
            os.environ.setdefault(name.strip(), value.strip().strip("'\""))


def release():
    """The commit the shop runs, so Sentry can tell which code an error came from."""
    try:
        return subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True,
                              check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def start():
    """Send errors, and messages logged as errors, to Sentry; without a DSN the shop runs as before."""
    load_env()
    logging.basicConfig(level=logging.INFO)
    dsn = os.environ.get("SENTRY_DSN")
    if not dsn:
        log.info("SENTRY_DSN is not set: errors are not sent to Sentry")
        return
    try:
        import sentry_sdk
    except ImportError:
        log.warning("SENTRY_DSN is set but sentry-sdk is not installed: pip install -r requirements.txt")
        return
    sentry_sdk.init(dsn=dsn, environment=os.environ.get("SENTRY_ENVIRONMENT", "demo"), release=release())
    log.info("Sending errors to Sentry")
