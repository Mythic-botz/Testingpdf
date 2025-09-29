# rename.py - File rename logic
from pyrogram import Client, filters
from helper import is_allowed_file, sanitize_filename, log_message, format_filename
from database import db
from config import CONFIG
import asyncio
import os

async def rename_handler(client: Client, message):
    """
    Handle incoming documents (PDFs).
    :param client: Pyrofork Client
    :param message: Incoming message
    """
    if not message.document or not is_allowed_file(message.document.file_name):
        return

    user_id = message.from_user.id
    username = message.from_user.username
    original_name = os.path.splitext(message.document.file_name)[0]
    await log_message(client, f"Received PDF from user {user_id}: {message.document.file_name}")

    # Get user format from DB
    format_pattern = db.get_user_setting(user_id, 'format_pattern', CONFIG['default_format_pattern'])

    # Prompt for custom name or use format
    await message.reply(
        f"Reply with new name for '{message.document.file_name}' "
        f"(or 'auto' for '{format_pattern}', 'default' for '{CONFIG['default_rename_pattern']}'):"
    )

    try:
        # Wait for reply
        replied_msg = await asyncio.wait_for(
            client.wait_for_message(message.chat.id, filters=filters.user(user_id) & filters.reply_to_message_id(message.id)),
            timeout=60
        )
        
        new_name = replied_msg.text.strip()
        if new_name.lower() == "auto":
            # Download file for chapter detection (if needed)
            file_path = await message.download()
            new_name = format_filename(format_pattern, original_name, user_id, username, file_path)
            if os.path.exists(file_path):
                os.remove(file_path)  # Clean up
        elif new_name.lower() == "default":
            new_name = CONFIG['default_rename_pattern'].format(original_name=original_name)
        else:
            new_name = new_name.format(original_name=original_name)
        
        new_name = sanitize_filename(new_name)
        
        # Send renamed document (simulated via caption)
        await client.send_document(
            chat_id=message.chat.id,
            document=message.document.file_id,
            caption=new_name,
            reply_to_message_id=message.id
        )
        
        db.set_user_setting(user_id, 'last_rename', new_name)
        await message.reply(f"Renamed to: {new_name}")
        
    except asyncio.TimeoutError:
        await message.reply("Timeout! Use /setformat to set auto-rename pattern.")
    except Exception as e:
        await log_message(client, f"Rename error for {user_id}: {e}")
        await message.reply("Error renaming. Try again.")