from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from config import BOT_TOKEN, PORT, SUDO_USERS
import os
import sys
import asyncio
from threading import Thread
from handlers import add_handlers
from helpers.filters import sudo_only
from aiohttp import web

async def web_server():
    async def handle(request):
        return web.Response(text="Web server is running")
    app = web.Application()
    app.router.add_get('/', handle)
    return app

async def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    if '-r' in sys.argv:
        for user in SUDO_USERS:
            application.bot.send_message(user, 'Restarted.')
    async def restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
        update.effective_message.reply_text('Restarting...')
        Thread(target=stop_and_restart, args=(update.effective_chat.id, update.effective_message.message_id,)).start()
    def stop_and_restart(chat, msg):
        application.stop()
        os.execl(sys.argv[0], *sys.argv)
    application.add_handler(CommandHandler('r', restart, sudo_only))
    add_handlers(application)
    try:
        app = web.AppRunner(await web_server())
        await app.setup()
        bind_address = "0.0.0.0"
        await web.TCPSite(app, bind_address, PORT).start()
        await application.run_polling()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await application.shutdown()

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main())
    except Exception as e:
        print(f"Error: {e}")
#    finally:
  #      loop.close()
