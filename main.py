import logging
from pyrofork import Client
from config import API_ID, API_HASH, BOT_TOKEN, WORKDIR

logging.basicConfig(level=logging.INFO)

app = Client(
    "AutoPdfRenameBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workdir=WORKDIR
)

if __name__ == "__main__":
    logging.info("🚀 Bot starting...")
    app.run()
