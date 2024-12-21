import logging
import nest_asyncio
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Дозволяємо повторний запуск циклу подій у середовищах на зразок Colab
nest_asyncio.apply()

# Логування
logging.basicConfig(level=logging.INFO)

# Токен
TOKEN = "7730295760:AAGuRYKPmnwhJospsWS4dbHW0yy3M6JrZRk"

# Дані вашого календаря
CALENDAR_ID = "3d1200d4f604504fd92ebc97ccf35ab40d52e1b014a79f9a0b4c61c0ec8dda0c@group.calendar.google.com"

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info(f"Отримано команду /start від {update.effective_user.username}")
    await update.message.reply_text(
        "Привіт! Я ваш бот. Ось список доступних команд:\n/help - Доступні команди\n"
    )

# Команда /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info(f"Отримано команду /help від {update.effective_user.username}")
    await update.message.reply_text(
        "Доступні команди:\n/start - Запустити бота\n/help - Доступні команди\n"
    )

# Обробник текстових повідомлень
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info(f"Отримано повідомлення: {update.message.text} від {update.effective_user.username}")
    await update.message.reply_text(f"Я отримав ваше повідомлення: {update.message.text}")

# Основна функція запуску бота
async def main():
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    
    print("Бот запущено. Зачекайте команди.")
    try:
        await application.run_polling()
    except KeyboardInterrupt:
        print("Робота бота була зупинена вручну.")

# Виклик асинхронної функції
if __name__ == "__main__":
    asyncio.run(main())
