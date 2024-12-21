import logging
import nest_asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import datetime
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# Дозволяємо повторний запуск циклу подій у Colab
nest_asyncio.apply()

# Логування
logging.basicConfig(level=logging.INFO)

# Токен
TOKEN = "ВАШ_ТОКЕН"

# Дані вашого календаря
CALENDAR_ID = "ВАШ_ID_КАЛЕНДАРЯ"

# Авторизація через файл облікових даних Google Calendar
def get_google_calendar_service():
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
    creds = Credentials.from_service_account_file("oberig-credentials.json", scopes=SCOPES)
    service = build('calendar', 'v3', credentials=creds)
    return service

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт! Ось доступні команди:\n/help - Допомога\n/rozklad - Розклад подій")

# Команда /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Команди:\n/start - Запуск бота\n/help - Допомога\n/rozklad - Розклад подій")

# Команда /rozklad
async def rozklad(update: Update, context: ContextTypes.DEFAULT_TYPE):
    events = get_calendar_events()
    if not events:
        await update.message.reply_text("Немає запланованих подій.")
    else:
        message = "📅 *Розклад подій:*\n\n"
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            start_time = datetime.datetime.fromisoformat(start).strftime('%d-%m-%Y %H:%M')
            message += f"• {event['summary']} (📆 {start_time})\n"
        await update.message.reply_text(message, parse_mode='Markdown')

# Основна функція запуску
async def main():
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("rozklad", rozklad))
    print("Бот запущено.")
    await application.run_polling()

# Виклик асинхронної функції
await main()
