import os
import logging
from telegram import Update
from telegram.ext import Application, ContextTypes, MessageHandler, filters

# ✅ 启用日志，方便调试
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ✅ 从环境变量获取 Bot 配置
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
A_ID = int(os.getenv("A_ID", "0"))
B_ID = int(os.getenv("B_ID", "0"))
C_ID = int(os.getenv("C_ID", "0"))

# ✅ 处理文档消息
async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    sender = message.from_user

    if not message or not sender or not message.document:
        return

    filename = message.document.file_name.lower()
    if not (
        filename.endswith(".xls")
        or filename.endswith(".xlsx")
        or filename.endswith(".csv")
        or filename.endswith(".txt")
    ):
        return

    if sender.id == A_ID:
        try:
            file = await message.document.get_file()
            caption = message.caption or ""

            # ✅ 转发文件
            await context.bot.send_document(chat_id=B_ID, document=file.file_id, caption=caption)
            await context.bot.send_document(chat_id=C_ID, document=file.file_id, caption=caption)

            # ✅ 回复确认
            await message.reply_text("A 收到")
            logger.info("文件已成功转发并回复 A 收到")
        except Exception as e:
            logger.error(f"❌ 文件转发失败: {e}")

# ✅ 主入口，run_webhook 方式
def main():
    if not BOT_TOKEN or not WEBHOOK_URL:
        raise ValueError("❌ 必须设置 BOT_TOKEN 和 WEBHOOK_URL 环境变量")

    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))

    # ✅ 启动 webhook
    application.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 8080)),
        webhook_url=WEBHOOK_URL
    )

if __name__ == '__main__':
    main()
