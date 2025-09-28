import os
import aiofiles

def safe_filename(name: str) -> str:
    return "".join(c if c.isalnum() or c in "._-" else "_" for c in name)

def ensure_dir(path: str):
    if not os.path.exists(path):
        os.makedirs(path)

async def download_message(message, path: str):
    await message.download(file_name=path)
    return path
