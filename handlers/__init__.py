from telegram.ext import Defaults, Updater
from . import abort
from . import host
from . import message
from . import next
from . import scores
from . import start
from . import view

HANDLERS = [
    abort.handler,
    host.handler,
    message.handler,
    next.handler,
    scores.handler,
    start.handler,
    view.handler,
]

def add_handlers(dp: Dispatcher) -> None:
    """Add handlers to the dispatcher."""
    for handler in HANDLERS:
        dp.add_handler(handler)
