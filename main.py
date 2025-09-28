import os
from datetime import datetime
from pytz import timezone
from pyrogram import Client, __version__
from pyrogram.raw.all import layer
from config import *
import pyrogram.utils

# Fix for chat/channel ID edge cases
pyrogram.utils.MIN_CHAT_ID = -999999999999
pyrogram.utils.MIN_CHANNEL_ID = -100999999999999

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="renamer",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            workers=200,
            plugins={"root": "plugins"},
            sleep_threshold=15,
        )

    async def start(self):
        await super().start()

        me = await self.get_me()
        self.mention = me.mention
        self.username = me.username
        self.uptime = BOT_UPTIME if "BOT_UPTIME" in globals() else None

        print(f"{me.first_name} is started.....✨️")

        # Notify admins
        for admin_id in ADMIN:
            try:
                await self.send_message(admin_id, f"**{me.first_name} is Started...**")
            except Exception:
                pass

        # Notify log channel
        if LOG_CHANNEL:
            try:
                curr = datetime.now(timezone("Asia/Kolkata"))
                date = curr.strftime('%d %B, %Y')
                time = curr.strftime('%I:%M:%S %p')
                await self.send_message(
                    LOG_CHANNEL,
                    f"**{self.mention} is Restarted !!**\n\n"
                    f"📅 Date : `{date}`\n"
                    f"⏰ Time : `{time}`\n"
                    f"🌐 Timezone : `Asia/Kolkata`\n\n"
                    f"🉐 Version : `v{__version__} (Layer {layer})`"
                )
            except Exception:
                print("Please make the bot an admin in your log channel.")

    async def stop(self, *args):
        await super().stop()
        print("✅ Bot stopped successfully.")


if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 8080))
    BASE_URL = os.environ.get("BASE_URL", None)  # your Render domain with https

    if not BASE_URL:
        raise Exception("❌ BASE_URL environment variable is required for webhook!")

    bot = Bot()

    webhook_url = f"{BASE_URL}/{WEBHOOK_PATH}"  # WEBHOOK_PATH in config.py
    print(f"🚀 Bot running in webhook mode at {webhook_url}")

    # Start webhook listener
    bot.run(
        web=True,
        host="0.0.0.0",
        port=PORT,
        webhook_url=webhook_url
    )
