from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, Application
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

def add_handlers(application: Application) -> None:
    """Add handlers to the application."""
    for handler in HANDLERS:
        application.add_handler(handler)
