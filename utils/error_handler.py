from telegram import Update
from telegram.ext import ContextTypes
from utils.logger import logger

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(msg="❌ Виникла помилка:", exc_info=context.error)
    await update.message.reply_text("❌ Виникла непередбачувана помилка. Спробуйте ще раз.")
