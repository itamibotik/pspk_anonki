from db import DB_FILE
import aiosqlite
from datetime import datetime, timedelta
from config import TARGET_CHANNEL_ID
from telegram.constants import ParseMode

async def generate_weekly_summary(bot):
    async with aiosqlite.connect(DB_FILE) as db:
        week_ago = (datetime.now() - timedelta(days=7)).isoformat()

        # Самая залайканная
        cursor = await db.execute('''
            SELECT message_id, MAX(likes)
            FROM (
                SELECT message_id,
                SUM(CASE WHEN vote = 1 THEN 1 ELSE 0 END) as likes
                FROM votes
                GROUP BY message_id
            )
        ''')
        most_liked = await cursor.fetchone()

        # Самая задизлайканная
        cursor = await db.execute('''
            SELECT message_id, MAX(dislikes)
            FROM (
                SELECT message_id,
                SUM(CASE WHEN vote = -1 THEN 1 ELSE 0 END) as dislikes
                FROM votes
                GROUP BY message_id
            )
        ''')
        most_disliked = await cursor.fetchone()

    text = "📊 Итоги недели:\n\n"

    if most_liked and most_liked[0]:
        text += f"🏆 Самая залайканная: [пост](https://t.me/c/{str(TARGET_CHANNEL_ID)[4:]}/{most_liked[0]}) — 👍 {most_liked[1]}\n"

    if most_disliked and most_disliked[0]:
        text += f"😈 Самая задизлайканная: [пост](https://t.me/c/{str(TARGET_CHANNEL_ID)[4:]}/{most_disliked[0]}) — 👎 {most_disliked[1]}\n"

    await bot.send_message(
        chat_id=TARGET_CHANNEL_ID,
        text=text,
        parse_mode=ParseMode.MARKDOWN
    )
