import os

# Bot Settings
API_ID = int(os.getenv("API_ID", "23476863"))
API_HASH = os.getenv("API_HASH", "69daa0835439c4211f34c2e9ad0acb5c")
BOT_TOKEN = os.getenv("BOT_TOKEN", "6809164496:AAGmTBe5dCMBFH4HG6zzON87MPKsOSzo6d4")

# Work directory for temp files
WORKDIR = "downloads"

# MongoDB
MONGO_URL = os.getenv("MONGO_URL", "mongodb+srv://Haruto179:Haruto179@cluster179.hy2mawo.mongodb.net/?retryWrites=true&w=majority&appName=Cluster179")
DB_NAME = "Haruto179"

# Dump channel (optional)
DUMP_CHANNEL_ID = int(os.getenv("DUMP_CHANNEL_ID", "0"))
