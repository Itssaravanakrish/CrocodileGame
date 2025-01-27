
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from helpers.wrappers import nice_errors
from mongo import users

@nice_errors
def callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle the '/scores' command.
    
    Send the user's total scores and scores in the current chat.
    """
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    
    total_user_scores = users.total_scores(user_id)
    scores_in_current_chat = users.scores_in_chat(chat_id, user_id) if update.effective_chat.type == 'supergroup' else '<code>not in group</code>'
    
    update.effective_message.reply_text(
        f'Your total scores: {total_user_scores}\nYour scores in this chat: {scores_in_current_chat}',
    )

handler = CommandHandler('scores', callback)
