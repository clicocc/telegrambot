import os
from telegram import Update
from telegram.ext import Application, ContextTypes, MessageHandler, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")
A_ID = int(os.getenv("A_ID"))  # ✅ A 的 Telegram user_id
B_ID = int(os.getenv("B_ID"))
C_ID = int(os.getenv("C_ID"))

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    sender = message.from_user

    if not message or not sender or not message.document:
        return

    filename = message.document.file_name.lower()
    if not (filename.endswith('.xls') or filename.endswith('.xlsx') or filename.endswith('.csv') or filename.endswith('.txt')):
        return

    if sender.id == A_ID:
        file = await message.document.get_file()
        caption = message.caption or ""
        await context.bot.send_document(chat_id=B_ID, document=file.file_id, caption=caption)
        await context.bot.send_document(chat_id=C_ID, document=file.file_id, caption=caption)
        await message.reply_text("A 收到")

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    application.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 8080)),
        webhook_url=os.environ["WEBHOOK_URL"]
    )

if __name__ == '__main__':
    main()
