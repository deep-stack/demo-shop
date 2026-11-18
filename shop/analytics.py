"""Events sent to the analytics service."""
from .outside import post

ANALYTICS_URL = "https://analytics.example.com/events"


def track_signup(email, city):
    """Record a new signup, with where the customer lives, for the marketing dashboard."""
    post(ANALYTICS_URL, {"event": "signup", "email": email, "city": city})
