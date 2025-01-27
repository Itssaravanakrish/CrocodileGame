from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import filters
import mongo.chats as db
from helpers.game import new_game
from helpers.wrappers import nice_errors

@nice_errors
def callback(update: Update, context: CallbackContext) -> None:
    """
    Handle the '/start' command in a group chat.
    
    Start a new game and update the database with the chat details.
    """
    new_game(update.effective_user, context)
    
    # Add try-except block for database update
    try:
        db.update(update.effective_chat.id, update.effective_chat.title)
    except Exception as e:
        print(f"Error updating database: {e}")
    
    update.effective_message.reply_text(
        f'{update.effective_user.mention_html()} talks about a word.',
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        'View',
                        callback_data='view',
                    ),
                ],
                [
                    InlineKeyboardButton(
                        'Next',
                        callback_data='next',
                    ),
                ],
            ]
        ),
    )

handler = CommandHandler('start', callback, filters.ChatType.GROUPS)
