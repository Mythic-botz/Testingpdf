import os
import shutil
from pyrogram import Client, filters
from config import WORKDIR, DUMP_CHANNEL_ID
from helper.database import Database
from helper.utils import download_message, safe_filename, ensure_dir
from plugins.thumbnail import make_pdf_thumbnail

db = Database()

@Client.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    txt = (
        "👋 Hi! I’m an **Auto PDF Rename Bot**.\n\n"
        "📌 Send me a PDF and I’ll rename it automatically.\n"
        "💡 You can set your rename format using:\n"
        "`/setformat MyBook_Chapter{num}.pdf`\n\n"
        "📷 Send an image to set it as your custom thumbnail."
    )
    await message.reply(txt)

@Client.on_message(filters.command("setformat") & filters.private)
async def set_format(client, message):
    user = message.from_user
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        return await message.reply("Usage: `/setformat NewName_{num}.pdf`", parse_mode="markdown")
    fmt = args[1]
    await db.set_format(user.id, fmt)
    await message.reply(f"✅ Format saved: `{fmt}`", parse_mode="markdown")

@Client.on_message(filters.private & filters.document)
async def auto_rename_pdf(client, message):
    user = message.from_user
    await db.ensure_user(user.id, getattr(user, "username", None))

    doc = message.document
    if not doc.file_name.lower().endswith(".pdf"):
        return await message.reply("⚠️ Only PDF files are supported!")

    fmt = await db.get_format(user.id)
    if not fmt:
        return await message.reply("⚠️ Please set a format first using `/setformat`")

    # Extract chapter number from filename (basic example)
    import re
    match = re.search(r"(\d+)", doc.file_name)
    num = match.group(1) if match else "1"

    new_name = fmt.format(num=num)
    new_name = safe_filename(new_name)

    ensure_dir(WORKDIR)
    orig_path = os.path.join(WORKDIR, f"{doc.file_id}_orig.pdf")
    new_path = os.path.join(WORKDIR, new_name)

    status = await message.reply("⬇️ Downloading PDF...")
    try:
        await download_message(message, orig_path)

        # try thumbnail
        thumb_id = await db.get_thumbnail(user.id)
        if not thumb_id:
            thumb_file = await make_pdf_thumbnail(orig_path)
        else:
            thumb_file = thumb_id

        shutil.copyfile(orig_path, new_path)

        await status.edit("⬆️ Uploading renamed PDF...")
        await client.send_document(
            chat_id=message.chat.id,
            document=new_path,
            thumb=thumb_file,
            caption=f"📄 Renamed: `{new_name}`",
            parse_mode="markdown"
        )

        if DUMP_CHANNEL_ID:
            await client.send_document(
                chat_id=DUMP_CHANNEL_ID,
                document=new_path,
                caption=f"Dump: {user.id}"
            )

        await db.log_file(message.chat.id, message.id, user.id, doc.file_name, new_name, doc.file_id)
        await status.delete()

    except Exception as e:
        await status.edit(f"❌ Error: {e}")
    finally:
        try: os.remove(orig_path)
        except: pass
