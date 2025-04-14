import aiosqlite
from datetime import datetime, timedelta

DB_FILE = "anonki.db"

async def init_db():
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS blocked_users (
                user_id INTEGER PRIMARY KEY
            )
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                chat_id INTEGER,
                username TEXT
            )
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS stats (
                date TEXT,
                user_id INTEGER,
                event_type TEXT
            )
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS published_anonki (
                message_id INTEGER PRIMARY KEY,
                user_id INTEGER,
                content TEXT,
                date TEXT
            )
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS filter_settings (
                word TEXT PRIMARY KEY
            )
        ''')
        await db.commit()

async def save_user(user_id, chat_id, username=None):
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute('''
            INSERT OR REPLACE INTO users (user_id, chat_id, username)
            VALUES (?, ?, ?)
        ''', (user_id, chat_id, username))
        await db.commit()

async def block_user(user_id):
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute('INSERT OR IGNORE INTO blocked_users VALUES (?)', (user_id,))
        await db.commit()

async def unblock_user(user_id):
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute('DELETE FROM blocked_users WHERE user_id = ?', (user_id,))
        await db.commit()

async def is_user_blocked(user_id):
    async with aiosqlite.connect(DB_FILE) as db:
        cursor = await db.execute('SELECT 1 FROM blocked_users WHERE user_id = ?', (user_id,))
        return await cursor.fetchone() is not None

async def log_event(user_id, event_type):
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute('INSERT INTO stats VALUES (?, ?, ?)',
                         (datetime.now().isoformat(), user_id, event_type))
        await db.commit()
