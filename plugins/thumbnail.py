import fitz  # PyMuPDF
from PIL import Image
from pyrogram import Client, filters
from helper.database import Database

db = Database()

async def make_pdf_thumbnail(pdf_path: str) -> str | None:
    try:
        doc = fitz.open(pdf_path)
        page = doc[0]
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
        thumb_path = pdf_path + ".jpg"
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        img.thumbnail((320, 320))
        img.save(thumb_path, "JPEG")
        return thumb_path
    except Exception:
        return None

@Client.on_message(filters.private & filters.photo)
async def save_user_thumbnail(client, message):
    user = message.from_user
    photo = message.photo
    await db.save_thumbnail(user.id, photo.file_id)
    await message.reply("✅ Your custom thumbnail has been saved!")
