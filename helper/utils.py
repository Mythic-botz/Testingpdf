# helper_utils.py - Utility functions
from pyrogram import Client
import os
import asyncio
from config import CONFIG
import re
import PyPDF2
from datetime import datetime

async def log_message(client: Client, message: str, user_id: int = None):
    """
    Log to admin channel.
    :param client: Pyrofork Client
    :param message: Text to log
    :param user_id: Optional user ID
    """
    if CONFIG['log_channel']:
        log_text = f"[{asyncio.get_event_loop().time()}] {message}" + (f" (User: {user_id})" if user_id else "")
        try:
            await client.send_message(CONFIG['log_channel'], log_text)
        except Exception as e:
            print(f"Log error: {e}")

def is_allowed_file(file_name: str) -> bool:
    """
    Check if file extension is allowed.
    :param file_name: File name
    :return: True if allowed
    """
    ext = os.path.splitext(file_name.lower())[1]
    return ext in CONFIG['allowed_file_types']

def sanitize_filename(name: str) -> str:
    """
    Clean filename and ensure PDF extension.
    :param name: Proposed name
    :return: Sanitized name
    """
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        name = name.replace(char, '_')
    return name[:100] + ".pdf" if not name.lower().endswith('.pdf') else name[:100]

def detect_chapter(file_name: str, file_path: str = None) -> str:
    """
    Detect chapter number from filename or PDF content.
    :param file_name: Original filename
    :param file_path: Local path to PDF (if available)
    :return: Chapter number as string (e.g., '01') or 'Unknown'
    """
    patterns = [
        r"[Cc]hapter[\s_-]*(\d+)",  # Chapter 01, Ch_1
        r"[Cc]h[\s_-]*(\d+)",      # Ch01, Ch 1
        r"[Ee]p[\s_-]*(\d+)",      # Ep01, Ep 1
        r"\b(\d+)\b"                # Fallback: Any number
    ]
    
    for pattern in patterns:
        match = re.search(pattern, file_name)
        if match:
            return f"{int(match.group(1)):02d}"
    
    if file_path and os.path.exists(file_path):
        try:
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                if len(reader.pages) > 0:
                    text = reader.pages[0].extract_text() or ""
                    for pattern in patterns:
                        match = re.search(pattern, text)
                        if match:
                            return f"{int(match.group(1)):02d}"
        except Exception as e:
            print(f"Chapter detection error: {e}")
    
    return "Unknown"

def format_filename(pattern: str, original_name: str, user_id: int, username: str = None, file_path: str = None) -> str:
    """
    Apply format pattern with variables.
    :param pattern: Format string (e.g., '{original_name}_Ch{chapter}')
    :param original_name: Original filename without extension
    :param user_id: Telegram user ID
    :param username: Telegram username
    :param file_path: Local path to PDF for chapter detection
    :return: Formatted filename
    """
    now = datetime.now()
    variables = {
        "original_name": original_name,
        "chapter": detect_chapter(original_name, file_path),
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H-%M-%S"),
        "user_id": str(user_id),
        "username": username or "NoUsername"
    }
    
    formatted = pattern
    for var, value in variables.items():
        formatted = formatted.replace(f"{{{var}}}", value)
    
    return sanitize_filename(formatted)