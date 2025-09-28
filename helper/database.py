import motor.motor_asyncio
import os
from config import MONGO_URL, DB_NAME

class Database:
    def __init__(self):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
        self.db = self.client[DB_NAME]
        self.users = self.db.users
        self.logs = self.db.logs

    async def ensure_user(self, user_id: int, username: str | None = None):
        await self.users.update_one(
            {"_id": user_id},
            {"$set": {"username": username}},
            upsert=True
        )

    async def save_thumbnail(self, user_id: int, file_id: str):
        await self.users.update_one(
            {"_id": user_id},
            {"$set": {"thumbnail_id": file_id}},
            upsert=True
        )

    async def get_thumbnail(self, user_id: int) -> str | None:
        user = await self.users.find_one({"_id": user_id})
        return user.get("thumbnail_id") if user else None

    async def set_format(self, user_id: int, fmt: str):
        await self.users.update_one(
            {"_id": user_id},
            {"$set": {"format": fmt}},
            upsert=True
        )

    async def get_format(self, user_id: int) -> str | None:
        user = await self.users.find_one({"_id": user_id})
        return user.get("format") if user else None

    async def log_file(self, chat_id, msg_id, user_id, old_name, new_name, file_id):
        await self.logs.insert_one({
            "chat_id": chat_id,
            "msg_id": msg_id,
            "user_id": user_id,
            "old_name": old_name,
            "new_name": new_name,
            "file_id": file_id
        })
