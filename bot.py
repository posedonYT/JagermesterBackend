import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import TOKEN, WEBAPP_URL
import logging

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

# Проверка наличия токена и URL
if not TOKEN:
    raise ValueError("No TOKEN provided in .env file")
if not WEBAPP_URL:
    raise ValueError("No WEBAPP_URL provided in .env file")

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера для aiogram 3.x
bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    # Создаем кнопку для открытия веб-приложения
    webapp_button = InlineKeyboardButton(
        text="Открыть игру",
        web_app=types.WebAppInfo(url=WEBAPP_URL)
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[webapp_button]])

    await message.answer(
        "Добро пожаловать в Jagermester combat",
        reply_markup=keyboard
    )