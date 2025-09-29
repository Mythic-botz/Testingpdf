# database.py - SQLite database handler for user settings
import sqlite3
import os
from typing import Optional, Dict

class Database:
    def __init__(self, db_path: str):
        """
        Initialize database connection.
        :param db_path: Path to SQLite file
        """
        self.db_path = db_path
        self.conn = None
        self.init_db()

    def init_db(self):
        """Create database and tables."""
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        cursor = self.conn.cursor()
        
        # Users table: Stores settings (rename_pattern, format_pattern)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                settings TEXT DEFAULT '{}'
            )
        """)
        
        # Thumbnails table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS thumbnails (
                user_id INTEGER PRIMARY KEY,
                thumbnail_path TEXT
            )
        """)
        
        self.conn.commit()
        print(f"Database initialized at {self.db_path}")

    def get_user_setting(self, user_id: int, key: str, default: str = "") -> str:
        """
        Get user setting (e.g., 'format_pattern').
        :param user_id: Telegram user ID
        :param key: Setting key (rename_pattern, format_pattern)
        :param default: Fallback value
        :return: Value as string
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT settings FROM users WHERE user_id = ?", (user_id,))
        result = cursor.fetchone()
        
        if result:
            import json
            settings = json.loads(result[0])
            return settings.get(key, default)
        return default

    def set_user_setting(self, user_id: int, key: str, value: str):
        """
        Set user setting.
        :param user_id: Telegram user ID
        :param key: Setting key
        :param value: Value to set
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT settings FROM users WHERE user_id = ?", (user_id,))
        result = cursor.fetchone()
        
        import json
        if result:
            settings = json.loads(result[0])
            settings[key] = value
            cursor.execute("UPDATE users SET settings = ? WHERE user_id = ?", (json.dumps(settings), user_id))
        else:
            settings = {key: value}
            cursor.execute("INSERT INTO users (user_id, settings) VALUES (?, ?)", (user_id, json.dumps(settings)))
        
        self.conn.commit()

    def get_thumbnail(self, user_id: int) -> Optional[str]:
        """Get user's thumbnail path."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT thumbnail_path FROM thumbnails WHERE user_id = ?", (user_id,))
        result = cursor.fetchone()
        return result[0] if result else None

    def set_thumbnail(self, user_id: int, path: str):
        """Set user's thumbnail path."""
        cursor = self.conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO thumbnails (user_id, thumbnail_path) VALUES (?, ?)", (user_id, path))
        self.conn.commit()

    def close(self):
        """Close connection."""
        if self.conn:
            self.conn.close()

db = None  # Initialized in main.py