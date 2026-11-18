"""Calls to the outside services the shop uses."""
import json
import logging
import urllib.request

log = logging.getLogger(__name__)


def post(url, payload):
    request = urllib.request.Request(url, data=json.dumps(payload).encode(),
                                     headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            return response.status
    except OSError:
        log.error("Could not send %s to %s", payload, url)
        raise
