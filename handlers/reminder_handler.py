import asyncio
from datetime import datetime, timedelta
from telegram import Bot
from calendar_utils import get_calendar_events
from utils.logger import logger

async def reminder(bot: Bot):
    while True:
        try:
            events = get_calendar_events()
            now = datetime.now()
            one_hour_later = now + timedelta(hours=1)
            
            for event in events:
                start = event["start"].get("dateTime", event["start"].get("date"))
                event_time = datetime.fromisoformat(start) if 'T' in start else datetime.strptime(start, '%Y-%m-%d')
                
                if now <= event_time <= one_hour_later:
                    message = (
                        f"⏰ **Нагадування про подію:**\n"
                        f"📅 {event_time.strftime('%d-%m-%Y')} — {event['summary']}\n"
                        f"🕒 Час початку: {event_time.strftime('%H:%M')}"
                    )
                    await bot.send_message(chat_id='YOUR_CHAT_ID', text=message)
                    logger.info(f"📲 Надіслано нагадування про подію: {event['summary']}")
            
            await asyncio.sleep(300)  # Перевірка кожні 5 хвилин
        except Exception as e:
            logger.error(f"❌ Помилка у функції нагадувань: {e}")
            await asyncio.sleep(300)
