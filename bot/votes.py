import aiosqlite
from config import TARGET_CHANNEL_ID
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

DB_FILE = "anonki.db"

async def add_vote(message_id, user_id, vote_value):
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute('''
            INSERT OR REPLACE INTO votes (message_id, user_id, vote)
            VALUES (?, ?, ?)
        ''', (message_id, user_id, vote_value))
        await db.commit()

async def get_votes(message_id):
    async with aiosqlite.connect(DB_FILE) as db:
        cursor = await db.execute('''
            SELECT
                SUM(CASE WHEN vote = 1 THEN 1 ELSE 0 END),
                SUM(CASE WHEN vote = -1 THEN 1 ELSE 0 END)
            FROM votes
            WHERE message_id = ?
        ''', (message_id,))
        result = await cursor.fetchone()
        return result or (0, 0)

def vote_keyboard(message_id, likes, dislikes):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(f"👍 {likes}", callback_data=f"like|{message_id}"),
            InlineKeyboardButton(f"👎 {dislikes}", callback_data=f"dislike|{message_id}")
        ]
    ])
