"""Calls to the outside services the shop uses."""
import json
import urllib.request


def post(url, payload):
    request = urllib.request.Request(url, data=json.dumps(payload).encode(),
                                     headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(request, timeout=10) as response:
        return response.status
