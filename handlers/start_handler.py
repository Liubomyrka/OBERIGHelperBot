from telegram import Update
from telegram.ext import ContextTypes
from utils.logger import logger

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("🔄 Виконання команди: /start")
    try:
        await update.message.reply_text(
            "👋 *Вітаю, я OBERIG Bot!* 🎵\n\n"
            "Я ваш вірний помічник.\n"
            "Використовуйте /help, щоб побачити доступні команди. 📋"
            "\n\n_Давайте почнемо! 🚀_",
            parse_mode='Markdown'
        )
        logger.info("✅ Команда /start виконана успішно")
    except Exception as e:
        logger.error(f"❌ Помилка у команді /start: {e}")
        await update.message.reply_text("❌ Виникла помилка при виконанні команди /start.")
