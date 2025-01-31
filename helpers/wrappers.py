from typing import Callable
from telegram import Update
from telegram.ext import CallbackContext
import logging

def admin_only(handler: Callable):
    """
    Decorator to restrict access to admin-only commands.

    Args:
        handler (Callable): The function to decorate.

    Returns:
        Callable: The decorated function.
    """
    def wrapper(update: Update, context: CallbackContext):
        if update.effective_chat.get_member(update.effective_user.id).status in ('creator', 'administrator'):
            return handler(update, context)
    return wrapper

def nice_errors(handler: Callable):
    """
    Decorator to catch and handle exceptions.

    Args:
        handler (Callable): The function to decorate.

    Returns:
        Callable: The decorated function.
    """
    def wrapper(update: Update, context: CallbackContext):
        try:
            return handler(update, context)
        except Exception as e:
            logging.error(f"Error: {e}")
            if update.callback_query:
                update.callback_query.answer(f'{e}', show_alert=True)
            else:
                update.effective_message.reply_text(f'Error: {e}')
    return wrapper
