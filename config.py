import os

# Bot Settings


# MongoDB
MONGO_URL = os.getenv("MONGO_URL", "mongodb+srv://Haruto179:Haruto179@cluster179.hy2mawo.mongodb.net/?retryWrites=true&w=majority&appName=Cluster179")
DB_NAME = "Haruto179"

# Dump channel (optional)
DUMP_CHANNEL_ID = int(os.getenv("DUMP_CHANNEL_ID", "0"))


# ------------------------------
# Webhook / deployment config
# ------------------------------


# config.py - Central configuration loader for the bot
import os

# Load environment variables
API_ID = int(os.getenv("API_ID", "23476863"))
API_HASH = os.getenv("API_HASH", "69daa0835439c4211f34c2e9ad0acb5c")
BOT_TOKEN = os.getenv("BOT_TOKEN", "6809164496:AAGmTBe5dCMBFH4HG6zzON87MPKsOSzo6d4")
DATABASE_PATH = os.getenv("DATABASE_PATH", "bot.db")
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "https://testingpdf.onrender.com")
PORT = int(os.getenv("PORT", "10000"))
ADMIN_IDS = [int(id.strip()) for id in os.getenv("ADMIN_IDS", "6617544956").split() if id.strip()]
LOG_CHANNEL = int(os.getenv("LOG_CHANNEL", "-1003060617678"))


# Default rename settings
DEFAULT_RENAME_PATTERN = "{original_name}_renamed.pdf"  # Fallback pattern
DEFAULT_FORMAT_PATTERN = "{original_name}_Ch{chapter}_{date}"  # Default format with variables
ALLOWED_FILE_TYPES = [".pdf", ".doc", ".docx"]

# Supported format variables (for /setformat)
FORMAT_VARIABLES = {
    "original_name": "Original filename without extension",
    "chapter": "Chapter number detected from filename or PDF",
    "date": "Current date (YYYY-MM-DD)",
    "time": "Current time (HH-MM-SS)",
    "user_id": "Telegram user ID",
    "username": "Telegram username (if available)"
}

# Validation
if API_ID == 0 or not API_HASH or not BOT_TOKEN:
    raise ValueError("Missing required env vars: API_ID, API_HASH, BOT_TOKEN")

CONFIG = {
    "api_id": API_ID,
    "api_hash": API_HASH,
    "bot_token": BOT_TOKEN,
    "database_path": DATABASE_PATH,
    "webhook_url": WEBHOOK_URL,
    "port": PORT,
    "admin_ids": ADMIN_IDS,
    "log_channel": LOG_CHANNEL,
    "default_rename_pattern": DEFAULT_RENAME_PATTERN,
    "default_format_pattern": DEFAULT_FORMAT_PATTERN,
    "allowed_file_types": ALLOWED_FILE_TYPES,
    "format_variables": FORMAT_VARIABLES
}

print("Config loaded:", {k: v if k not in ['api_hash', 'bot_token'] else "HIDDEN" for k, v in CONFIG.items()})
