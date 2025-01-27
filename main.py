from telegram.ext import Defaults, Updater
from config import BOT_TOKEN, PORT
from config import SUDO_USERS
import os
import sys
from threading import Thread
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler
from telegram.ext.updater import Dispatcher
from handlers import add_handlers
from helpers.filters import sudo_only
import asyncio
from aiohttp import web

async def web_server():
    async def handle(request):
        return web.Response(text="Web server is running")

    app = web.Application()
    app.router.add_get('/', handle)
    return app

async def main():
    defaults = Defaults(
        parse_mode='HTML',
        disable_web_page_preview=True,
        quote=False,
        run_async=True,
    )

    updater = Updater(token=BOT_TOKEN, defaults=defaults)
    dp: Dispatcher = updater.dispatcher

    if '-r' in sys.argv:
        for user in SUDO_USERS:
            updater.bot.send_message(user, 'Restarted.')

    def stop_and_restart(chat, msg):
        updater.stop()
        os.execl(sys.executable, sys.executable, *sys.argv, '-r', f'{chat}_{msg}', )

    async def restart(update: Update, context: CallbackContext):
        update.effective_message.reply_text('Restarting...')
        Thread(target=stop_and_restart, args=(update.effective_chat.id, update.effective_message.message_id,)).start()

    dp.add_handler(CommandHandler('r', restart, sudo_only))
    add_handlers(dp)

    app = web.AppRunner(await web_server())
    await app.setup()

    bind_address = "0.0.0.0"
    await web.TCPSite(app, bind_address, PORT).start()

    updater.start_polling(drop_pending_updates=True)
    await asyncio.idle()

if __name__ == '__main__':
    asyncio.run(main())
