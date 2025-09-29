import asyncio
import logging
import sqlite3
import requests
from pyrogram import Client

# Configure logging for better debugging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("bot.log"),  # Save logs to a file
        logging.StreamHandler()  # Also print logs to console
    ]
)
logger = logging.getLogger(__name__)

# Configuration (replace with your actual values or use environment variables)
CONFIG = {
    "api_id": "your_api_id",
    "api_hash": "your_api_hash",
    "bot_token": "your_bot_token",
    "webhook_url": "https://your-service.onrender.com/webhook"
}

def init_db():
    """Initialize SQLite database."""
    try:
        conn = sqlite3.connect("bot.db")
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)")
        conn.commit()
        logger.info("Database initialized at bot.db")
    except sqlite3.Error as e:
        logger.error(f"Database initialization failed: {e}")
    finally:
        conn.close()

async def set_webhook_manually(client, webhook_url):
    """Set Telegram webhook using HTTP request."""
    try:
        bot_token = CONFIG["bot_token"]
        url = f"https://api.telegram.org/bot{bot_token}/setWebhook?url={webhook_url}"
        response = requests.get(url)
        if response.status_code == 200:
            logger.info("Webhook set successfully")
        else:
            logger.error(f"Failed to set webhook: {response.text}")
    except Exception as e:
        logger.error(f"Error setting webhook: {e}")

async def main():
    """Main function to run the bot."""
    # Initialize database
    init_db()

    # Create Pyrogram client
    async with Client(
        "my_bot",
        api_id=CONFIG["api_id"],
        api_hash=CONFIG["api_hash"],
        bot_token=CONFIG["bot_token"]
    ) as app:
        try:
            # Set webhook
            await set_webhook_manually(app, CONFIG["webhook_url"])
            logger.info("Bot started, waiting for updates...")

            # Simulate running the bot (replace with your webhook server logic)
            # For example, you might run an aiohttp server here to handle updates
            await asyncio.sleep(3600)  # Keeps the bot running; adjust as needed
        except Exception as e:
            logger.error(f"Error in main loop: {e}")
        finally:
            logger.info("Shutting down bot...")

if __name__ == "__main__":
    # Use a single event loop for all async operations
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
    finally:
        # Ensure the loop is closed properly
        if not loop.is_closed():
            loop.close()
            logger.info("Event loop closed")        variables = "\n".join([f"{k}: {v}" for k, v in CONFIG["format_variables"].items()])
        return await message.reply(
            f"Usage: /setformat <pattern>\nAvailable variables:\n{variables}"
        )
    
    pattern = message.text.split(" ", 1)[1]
    user_id = message.from_user.id
    db.set_user_setting(user_id, 'format_pattern', pattern)
    await message.reply(f"Format set: {pattern}")
    await log_message(client, f"User {user_id} set format: {pattern}")

# Webhook
@flask_app.route(f"/webhook", methods=["POST"])
def webhook():
    if CONFIG["webhook_url"] == "":
        abort(403)
    
    update = request.get_json(force=True)
    asyncio.create_task(process_update(update))
    return "OK", 200

async def process_update(update):
    if "message" in update and update["message"].get("document"):
        mock_client = app
        mock_message = type('obj', (object,), update["message"])()
        await rename_handler(mock_client, mock_message)
    elif "message" in update and update["message"].get("text", "").startswith("/setformat"):
        mock_client = app
        mock_message = type('obj', (object,), update["message"])()
        await set_format(mock_client, mock_message)

async def main():
    await app.start()
    
    if CONFIG["webhook_url"]:
        await app.set_webhook(CONFIG["webhook_url"])
        print(f"Webhook set to {CONFIG['webhook_url']}")
        flask_app.run(host="0.0.0.0", port=CONFIG["port"], debug=False)
    else:
        print("Polling mode...")
        await app.idle()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    finally:
        db.close()
        app.stop()
