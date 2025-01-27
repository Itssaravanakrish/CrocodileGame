from telegram import Update
from telegram.ext import CallbackContext, CommandHandler
from helpers.game import end_game
from helpers.wrappers import admin_only
import logging

@admin_only
def callback(update: Update, context: CallbackContext) -> None:
    try:
        end_game(context)
        update.effective_message.reply_text(
            f'{update.effective_user.mention_html()} aborted the game.',
        )
    except Exception as e:
        logging.error(f'Error aborting game: {e}')
        update.effective_message.reply_text(f'Error: {e}')

handler = CommandHandler('abort', callback)
