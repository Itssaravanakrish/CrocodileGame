
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CallbackQueryHandler
from helpers.game import get_game
from helpers.wrappers import nice_errors

@nice_errors
def callback(update: Update, context: CallbackContext) -> None:
    """
    Handle the 'view' button press in a game.
    
    If the user is the host, send the game word as an alert. Otherwise, send a message indicating that the button is not for them.
    """
    game = get_game(context)
    if game['host'].id == update.effective_user.id:
        update.callback_query.answer(game['word'], True)
    else:
        update.callback_query.answer('This is not for you.', True)

handler = CallbackQueryHandler(callback, pattern='view')
