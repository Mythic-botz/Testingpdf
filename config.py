import os

# Bot Settings
API_ID = int(os.getenv("API_ID", "12345"))
API_HASH = os.getenv("API_HASH", "abc123")
BOT_TOKEN = os.getenv("BOT_TOKEN", "token_here")

# Work directory for temp files
WORKDIR = "downloads"

# MongoDB
MONGO_URL = os.getenv("MONGO_URL", "")
DB_NAME = "AutoPDFRename"

# Dump channel (optional)
DUMP_CHANNEL_ID = int(os.getenv("DUMP_CHANNEL_ID", "0"))
