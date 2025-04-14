from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_admin_keyboard(user_id):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ Одобрить", callback_data=f"send|{user_id}"),
            InlineKeyboardButton("⛔ Заблокировать", callback_data=f"block|{user_id}"),
            InlineKeyboardButton("📨 Ответить", callback_data=f"reply|{user_id}")
        ]
    ])
