# thumbnail.py - Handles thumbnail generation and attachment for renamed files
# Usage: Import Thumbnail; thumb = Thumbnail(); thumb_path = thumb.generate_or_get(client, user_id, message)

from PIL import Image
import os
from pyrogram import Client
from helper.helper_utils import log_message  # Updated import

class Thumbnail:
    def __init__(self):
        """
        Thumbnail manager.
        Generates a default if none set, or uses user-specific.
        """
        self.default_thumb_path = "default_thumb.jpg"  # Create a default image file locally

    async def generate_or_get(self, client: Client, user_id: int, message) -> str:
        """
        Get or generate thumbnail for the file.
        :param client: Pyrofork Client
        :param user_id: User ID
        :param message: Incoming message with file
        :return: Local path to thumbnail (or None)
        """
        # Check DB for user thumbnail
        from database import db
        thumb_path = db.get_thumbnail(user_id)
        
        if not thumb_path:
            # Generate default thumbnail (e.g., simple PDF icon)
            thumb_path = self._generate_default()
            db.set_thumbnail(user_id, thumb_path)
            await log_message(client, f"Generated default thumbnail for user {user_id}")
        
        # Validate path exists
        if os.path.exists(thumb_path):
            return thumb_path
        
        # Fallback: Extract from message if video/image, but for PDF, use default
        return None

    def _generate_default(self) -> str:
        """
        Create a simple default thumbnail (PDF icon placeholder).
        :return: Path to generated image
        """
        # Create a 320x320 white image with "PDF" text (Telegram thumbnail size)
        img = Image.new('RGB', (320, 320), color='white')
        from PIL import ImageDraw, ImageFont
        draw = ImageDraw.Draw(img)
        
        # Simple text (use default font; for better, download a TTF)
        try:
            font = ImageFont.truetype("arial.ttf", 50)  # Assumes system font
        except:
            font = ImageFont.load_default()
        
        draw.text((100, 140), "PDF", fill='black', font=font)
        
        path = "default_thumb.jpg"
        img.save(path)
        return path

    async def attach_thumbnail(self, client: Client, message, thumb_path: str):
        """
        Helper to send file with thumbnail.
        :param client: Pyrofork Client
        :param message: Reply-to message
        :param thumb_path: Path to thumbnail
        """
        if thumb_path and os.path.exists(thumb_path):
            # Send with thumb
            await client.send_document(
                chat_id=message.chat.id,
                document=message.document.file_id,
                reply_to_message_id=message.id,
                thumb=thumb_path
            )
        else:
            await client.send_document(
                chat_id=message.chat.id,
                document=message.document.file_id,
                reply_to_message_id=message.id
            )
