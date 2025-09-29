# main.py - Bot entry point
import os
import asyncio
from pyrogram import Client, filters
from flask import Flask, request, abort
from config import CONFIG
from helper.database import Database, db
from plugins.rename import rename_handler
from plugins.thumbnail import Thumbnail
from helper.utils import log_message  # Updated import

app = Client(
    "pdf_rename_bot",
    api_id=CONFIG["api_id"],
    api_hash=CONFIG["api_hash"],
    bot_token=CONFIG["bot_token"],
    plugins={"root": "plugins"}
)

flask_app = Flask(__name__)
thumb_manager = Thumbnail()
db = Database(CONFIG["database_path"])
db.init_db()

# Handlers
@app.on_message(filters.document & filters.private)
async def handle_document(client, message):
    await rename_handler(client, message)

@app.on_message(filters.command("setformat") & filters.private)
async def set_format(client: Client, message):
    """
    Set custom filename format.
    Usage: /setformat {original_name}_Ch{chapter}_{date}
    """
    if len(message.command) < 2:
        variables = "\n".join([f"{k}: {v}" for k, v in CONFIG["format_variables"].items()])
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
