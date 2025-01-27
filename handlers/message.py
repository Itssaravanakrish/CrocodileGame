
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import filters
from telegram.ext import MessageHandler
import mongo.users as db
from helpers.game import get_game
from helpers.game import is_true
from helpers.wrappers import nice_errors

# Define inline keyboard markup as a separate variable
inline_keyboard_markup = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                'I want to be the host',
                callback_data='host',
            ),
        ],
    ]
)

@nice_errors
def callback(update: Update, context: CallbackContext) -> None:
    """
    Handle user guesses in a game.
    
    If the user guesses the correct word, update the database and send a reply with an inline keyboard.
    """
    try:
        game = get_game(context)
        if game['host'].id != update.effective_user.id:
            if is_true(update.effective_message.text, context):
                update.effective_message.reply_text(
                    f"{update.effective_user.mention_html()} guessed the correct word, {game['word']}.",
                    reply_markup=inline_keyboard_markup,
                )
                # Add try-except block for database update
                try:
                    db.update(
                        update.effective_chat.id,
                        update.effective_user.id,
                        update.effective_user.first_name,
                        update.effective_user.username,
                    )
                except Exception as e:
                    print(f"Error updating database: {e}")
    except Exception as e:
        print(f"Error handling user guess: {e}")

handler = MessageHandler(
    filters.TEXT & ~filters.COMMAND & filters.ChatType.SUPERGROUP,
    callback,
)
