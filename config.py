import os
from dotenv import load_dotenv

# Загрузка переменных окружения из файла .env
load_dotenv()

TOKEN = os.getenv("TOKEN")
WEBAPP_URL = os.getenv("WEBAPP_URL")