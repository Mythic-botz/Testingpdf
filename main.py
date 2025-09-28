import os
from datetime import datetime
from pytz import timezone
from pyrogram import Client, __version__
from pyrogram.raw.all import layer
from aiohttp import web
from config import *
import pyrogram.utils

# Fix chat/channel ID edge cases
pyrogram.utils.MIN_CHAT_ID = -999999999999
pyrogram.utils.MIN_CHANNEL_ID = -100999999999999

# Initialize bot
bot = Client(
    name="renamer",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=200,
    plugins={"root": "plugins"},
    sleep_threshold=15,
)

# Webhook listener
async def handle_webhook(request):
    data = await request.json()
    await bot.process_updates([data])
    return web.Response(text="ok")

# Startup tasks
async def on_startup(app):
    await bot.start()
    me = await bot.get_me()
    bot.mention = me.mention
    bot.username = me.username
    print(f"🚀 {me.first_name} started in webhook mode!")

    # Notify admins
    for admin_id in ADMIN:
        try:
            await bot.send_message(admin_id, f"**{me.first_name} is Started...**")
        except Exception:
            pass

    # Notify log channel
    if LOG_CHANNEL:
        try:
            curr = datetime.now(timezone("Asia/Kolkata"))
            date = curr.strftime('%d %B, %Y')
            time = curr.strftime('%I:%M:%S %p')
            await bot.send_message(
                LOG_CHANNEL,
                f"**{bot.mention} is Restarted !!**\n\n"
                f"📅 Date : `{date}`\n"
                f"⏰ Time : `{time}`\n"
                f"🌐 Timezone : `Asia/Kolkata`\n\n"
                f"🉐 Version : `v{__version__} (Layer {layer})`"
            )
        except Exception:
            print("Please make the bot an admin in your log channel.")

# Shutdown tasks
async def on_cleanup(app):
    await bot.stop()
    print("✅ Bot stopped successfully.")

# Create aiohttp app
app = web.Application()
app.router.add_post(f"/{WEBHOOK_PATH}", handle_webhook)
app.on_startup.append(on_startup)
app.on_cleanup.append(on_cleanup)

if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 8080))
    BASE_URL = os.environ.get("BASE_URL")
    if not BASE_URL:
        raise Exception("❌ BASE_URL environment variable required for webhook!")

    print(f"🚀 Webhook listening at {BASE_URL}/{WEBHOOK_PATH}")
    web.run_app(app, host="0.0.0.0", port=PORT)
