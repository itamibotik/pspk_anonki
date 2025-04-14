from telegram import InlineKeyboardMarkup, InlineKeyboardButton

def get_fileshare_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📚 Шпора", callback_data="tag_spora"),
            InlineKeyboardButton("📄 Конспект", callback_data="tag_konspekt"),
            InlineKeyboardButton("📂 Файл", callback_data="tag_file")
        ]
    ])
