"""One of the shop's routes as a Vercel function: the shop's own handler answers it."""
from shop import monitoring
from shop.server import Handler

monitoring.start()


class handler(Handler):
    pass
