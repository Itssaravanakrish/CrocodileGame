
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CallbackQueryHandler
from helpers.game import get_game
from helpers.game import next_word
from helpers.wrappers import nice_errors

@nice_errors
def callback(update: Update, context: CallbackContext) -> None:
    """
    Handle the 'next' button press in a game.
    
    If the user is the host, send the next word as an alert. Otherwise, send a message indicating that the button is not for them.
    """
    game = get_game(context)
    if game['host'].id == update.effective_user.id:
        next_word_result = next_word(context)
        update.callback_query.answer(next_word_result, show_alert=True)
    else:
        update.callback_query.answer('This is not for you.', True)

handler = CallbackQueryHandler(callback, pattern='next')
