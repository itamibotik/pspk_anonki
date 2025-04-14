from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from telegram import Update
from config import TOKEN
from db import init_db
from anonki_manager import add_message_to_queue
from admin_tools import get_admin_post_keyboard, format_admin_message
from fileshare import get_fileshare_keyboard
from weekly_summary import generate_weekly_summary

async def start(update: Update, context):
    await update.message.reply_text(
        "Привет! Это бот анонимок pspk_anonki.\n\nВыбери действие:",
        reply_markup=get_admin_post_keyboard()
    )

async def handle_text(update: Update, context):
    user = update.message.from_user
    add_message_to_queue(user.id, update.message.text)
    await update.message.reply_text("✅ Анонка отправлена на модерацию!")

async def handle_callback(update: Update, context):
    query = update.callback_query
    await query.answer()

    if query.data.startswith("post_"):
        role = query.data.replace("post_", "").replace("owner", "Владелец").replace("tech", "Тех админ").replace("admin1", "Админ 1").replace("admin2", "Админ 2")
        await query.edit_message_text("Отправь текст сообщения:")
        context.user_data["post_role"] = role

async def handle_post_message(update: Update, context):
    if "post_role" not in context.user_data:
        return

    role = context.user_data["post_role"]
    text = update.message.text
    await context.bot.send_message(
        chat_id=context.bot_data["TARGET_CHANNEL_ID"],
        text=format_admin_message(role, text),
        parse_mode="HTML"
    )
    await update.message.reply_text("✅ Сообщение отправлено!")
    del context.user_data["post_role"]

async def start_bot():
    await init_db()

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("summary", lambda u, c: generate_weekly_summary(c.bot)))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_handler(MessageHandler(filters.TEXT & filters.UserStatus.ADMINISTRATOR, handle_post_message))

    app.run_polling()
