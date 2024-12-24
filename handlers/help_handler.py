from telegram import Update
from telegram.ext import ContextTypes
from utils.logger import logger

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("🔄 Виконання команди: /help")
    try:
        await update.message.reply_text(
            "📋 *Список доступних команд:*\n"
            "➡️ /start – *Вітання та інструкція*\n"
            "➡️ /help – *Переглянути список команд*\n"
            "➡️ /rozklad – *Переглянути розклад подій* 📅\n\n"
            "_Виберіть команду, щоб продовжити!_ 🚀",
            parse_mode='Markdown'
        )
        logger.info("✅ Команда /help виконана успішно")
    except Exception as e:
        logger.error(f"❌ Помилка у команді /help: {e}")
        await update.message.reply_text("❌ Виникла помилка при виконанні команди /help.")
