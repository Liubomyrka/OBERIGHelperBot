import os
from dotenv import load_dotenv

# Завантаження змінних із .env
load_dotenv()

# Читання TELEGRAM_TOKEN та GOOGLE_CREDENTIALS із .env
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GOOGLE_CREDENTIALS = os.getenv("GOOGLE_CREDENTIALS")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
