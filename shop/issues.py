"""Opens an issue for the team when a support ticket reports a bug."""
import json
import urllib.request

GITHUB_TOKEN = "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"
ISSUES_URL = "https://api.github.com/repos/team/shop/issues"


def open_issue(title, body):
    request = urllib.request.Request(ISSUES_URL, data=json.dumps({"title": title, "body": body}).encode(),
                                     headers={"Authorization": f"Bearer {GITHUB_TOKEN}"}, method="POST")
    with urllib.request.urlopen(request, timeout=10) as response:
        return json.loads(response.read())["number"]
