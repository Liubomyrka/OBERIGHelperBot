# main.py

import asyncio
from telegram import BotCommand, Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from handlers.start_handler import start
from handlers.help_handler import help_command
from handlers.schedule_handler import (
    schedule_command,
    set_reminder,
    unset_reminder,
    event_details_callback,
)
from utils.logger import logger


# 🛡️ Логування виконання команд
async def log_command(command_name: str, success: bool):
    if success:
        logger.info(f"✅ Виконано команду: {command_name}")
    else:
        logger.warning(f"❌ Помилка під час виконання команди: {command_name}")


# 🛡️ Обробник невідомих команд
async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.warning("⚠️ Отримана невідома команда")
    if update.effective_chat.type != "private":
        await update.message.reply_text(
            "❗ Ця команда доступна лише в особистих повідомленнях. "
            "[Напишіть мені в приватний чат](https://t.me/OBERIGHelperBot).",
            parse_mode="Markdown"
        )
    else:
        await help_command(update, context)
    logger.info("✅ Обробка невідомої команди завершена")


# 🛡️ Глобальний обробник помилок
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"❌ Виникла помилка: {context.error}")
    if update and hasattr(update, 'message'):
        await update.message.reply_text(
            "❌ Виникла внутрішня помилка. Адміністратор уже сповіщений."
        )


# 🛡️ Основна функція запуску
async def main():
    logger.info("🔄 Запуск основного додатка...")

    application = ApplicationBuilder().token("7730295760:AAF7Os85EY6E-ucV7vVJ48JVSovPjF-DyTA").build()
    
    # Команди для меню бота
    logger.info("🔧 Встановлення команд меню для бота...")
    await application.bot.set_my_commands([
        BotCommand("start", "Вітання та інструкція"),
        BotCommand("help", "Переглянути список команд"),
        BotCommand("rozklad", "Переглянути розклад подій"),
        BotCommand("reminder_on", "Увімкнути нагадування"),
        BotCommand("reminder_off", "Вимкнути нагадування"),
    ], scope=None)
    logger.info("✅ Команди меню встановлено успішно")

    # 🛡️ Додавання обробників команд
    logger.info("🔧 Додавання обробників команд...")

    application.add_handler(CommandHandler("start", start))
    logger.info("✅ Додано обробник команди: /start")

    application.add_handler(CommandHandler("help", help_command))
    logger.info("✅ Додано обробник команди: /help")

    application.add_handler(CommandHandler("rozklad", schedule_command))
    logger.info("✅ Додано обробник команди: /rozklad")

    application.add_handler(CommandHandler("reminder_on", set_reminder))
    logger.info("✅ Додано обробник команди: /reminder_on")

    application.add_handler(CommandHandler("reminder_off", unset_reminder))
    logger.info("✅ Додано обробник команди: /reminder_off")

    application.add_handler(CallbackQueryHandler(event_details_callback, pattern="^event_details_.*$"))
    logger.info("✅ Додано обробник callback-запитів для деталей подій")

    # 🛡️ Обробка невідомих команд
    application.add_handler(MessageHandler(filters.COMMAND, unknown_command))
    logger.info("✅ Додано обробник невідомих команд")

    # 🛡️ Глобальний обробник помилок
    application.add_error_handler(error_handler)
    logger.info("✅ Додано глобальний обробник помилок")

    logger.info("✅ *OBERIG Bot запущено успішно!* 🚀\n🔄 Очікую на команди від користувачів...")

    try:
        await application.run_polling()
    except Exception as e:
        logger.error(f"❌ Критична помилка при запуску бота: {e}")


# 🛡️ Запуск програми
if __name__ == "__main__":
    import nest_asyncio

    try:
        logger.info("🔄 Ініціалізація asyncio...")
        nest_asyncio.apply()
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🛑 Бот зупинено користувачем.")
    except RuntimeError as e:
        if "already running" in str(e):
            logger.warning("⚠️ Event loop is already running.")
            loop = asyncio.get_event_loop()
            loop.run_until_complete(main())
        else:
            raise e
