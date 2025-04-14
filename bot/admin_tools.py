from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from config import TARGET_CHANNEL_ID

def get_admin_post_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("👑 Владелец", callback_data="post_owner"),
            InlineKeyboardButton("🛠 Тех админ", callback_data="post_tech"),
            InlineKeyboardButton("📝 Админ 1", callback_data="post_admin1"),
            InlineKeyboardButton("📝 Админ 2", callback_data="post_admin2")
        ]
    ])

def format_admin_message(role, text):
    return f"✉️ <b>{role}</b>:\n{text}"
