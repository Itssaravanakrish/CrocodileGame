
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CallbackQueryHandler
import mongo.chats as db
from helpers.game import new_game
from helpers.wrappers import nice_errors

# Define inline keyboard markup as a separate variable
inline_keyboard_markup = InlineKeyboardMarkup(
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
)

@nice_errors
def callback(update: Update, context: CallbackContext) -> None:
    new_game(update.effective_user, context)
    update.effective_message.reply_text(
        f'{update.effective_user.mention_html()} talks about a word.',
        reply_markup=inline_keyboard_markup,
    )
    
    # Add try-except block for database update
    try:
        db.update(update.effective_chat.id, update.effective_chat.title)
    except Exception as e:
        print(f"Error updating database: {e}")
    
    update.callback_query.answer()

handler = CallbackQueryHandler(callback, pattern='host')
