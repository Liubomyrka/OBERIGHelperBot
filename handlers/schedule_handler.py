# schedule_handler.py

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils.calendar_utils import get_calendar_events
from datetime import datetime, timezone

# Словник для статусу нагадувань
user_reminders = {}
notified_events = set()  # Множина для зберігання ID подій, для яких вже надіслано нагадування


# 🛡️ Перевірка приватного чату
async def ensure_private_chat(update: Update, context: ContextTypes.DEFAULT_TYPE, command: str):
    """
    Перевіряє, чи команда виконується у приватному чаті.
    Якщо ні — перенаправляє користувача у приватний чат і автоматично виконує команду.
    """
    if update.effective_chat.type != "private":
        try:
            await context.bot.send_message(
                chat_id=update.effective_user.id,
                text=f"🔒 Ця команда доступна лише в особистих повідомленнях. Виконую команду: /{command}"
            )
            await update.message.reply_text(
                "📩 Відповів вам в особистому чаті. [Відкрити чат з ботом](https://t.me/OBERIGHelperBot)",
                parse_mode="Markdown"
            )
            await context.bot.send_message(
                chat_id=update.effective_user.id,
                text=f"/{command}"
            )
        except:
            await update.message.reply_text(
                "❗ Ця команда доступна лише в особистих повідомленнях. "
                "[Натисніть тут, щоб відкрити чат зі мною](https://t.me/OBERIGHelperBot)",
                parse_mode="Markdown"
            )
        return False
    return True


# 🛡️ Функція schedule_command
# """Відображає список подій з можливістю натискання на їх назви для перегляду деталей."""
async def schedule_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await ensure_private_chat(update, context, "rozklad"):
        return

    try:
        events = get_calendar_events()
        if not events:
            await update.message.reply_text("📅 Немає запланованих подій.")
        else:
            response = "📅 **Розклад подій:**\n──────────────\n"

            buttons = []
            for index, event in enumerate(events[:5], start=1):
                event_id = event.get("id")
                summary = event.get("summary", "Без назви")
                start = event["start"].get("dateTime", event["start"].get("date"))

                if 'T' in start:
                    dt = datetime.fromisoformat(start)
                    start_date = dt.strftime('%d-%m-%Y')
                    start_time = dt.strftime('%H:%M')
                else:
                    dt = datetime.strptime(start, '%Y-%m-%d')
                    start_date = dt.strftime('%d-%m-%Y')
                    start_time = "Весь день"

                response += (
                    f"{index}️⃣ *{summary}*\n"
                    f"📅 {start_date} ⏰ {start_time}\n"
                    f"──────────────\n"
                )
                # Додамо кнопку як inline, але текстовий варіант
                buttons.append([
                    InlineKeyboardButton(
                        text=f"ℹ️ {summary}",
                        callback_data=f"event_details_{event_id[:20]}"
                    )
                ])

            await update.message.reply_text(
                text=response,
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(buttons)
            )
    except Exception as e:
        await update.message.reply_text(f"❌ Помилка під час отримання подій: {e}")


# 🛡️ Функція event_details_callback
# """Виводить деталі події у відповідь на callback-запит."""
async def event_details_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    try:
        event_id = query.data.replace("event_details_", "")
        events = get_calendar_events()
        event = next((e for e in events if e.get("id", "").startswith(event_id)), None)

        if event:
            description = event.get("description", "Опис відсутній.")
            start = event["start"].get("dateTime", event["start"].get("date"))

            if 'T' in start:
                dt = datetime.fromisoformat(start)
                start_date = dt.strftime('%d-%m-%Y')
                start_time = dt.strftime('%H:%M')
            else:
                dt = datetime.strptime(start, '%Y-%m-%d')
                start_date = dt.strftime('%d-%m-%Y')
                start_time = "Весь день"

            response = (
                f"📅 **Деталі події:**\n"
                f"📌 **Назва:** {event['summary']}\n"
                f"📅 **Дата:** {start_date}\n"
                f"⏰ **Час:** {start_time}\n"
                f"📝 **Опис:** {description}"
            )
            await query.message.reply_text(text=response, parse_mode="Markdown")
        else:
            await query.message.reply_text("❌ Подію не знайдено.")
    except Exception as e:
        await query.message.reply_text(f"❌ Помилка: {e}")


# 🔔 Увімкнення нагадувань
async def set_reminder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await ensure_private_chat(update, context, "reminder_on"):
        return

    chat_id = update.effective_chat.id
    await update.message.reply_text("🔔 Нагадування увімкнено. Ви отримаєте сповіщення за 1 годину до події.")


# 🔕 Вимкнення нагадувань
async def unset_reminder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await ensure_private_chat(update, context, "reminder_off"):
        return

    chat_id = update.effective_chat.id
    await update.message.reply_text("🔕 Нагадування вимкнено.")
