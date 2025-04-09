import uvicorn
import asyncio
from bot import dp, bot
from api import app
import multiprocessing


def run_api():
    uvicorn.run(app, host="44.226.145.213", port=4000)


async def run_bot():
    # Запуск бота
    await dp.start_polling(bot)


def bot_process_func():
    asyncio.run(run_bot())


if __name__ == "__main__":
    # Запускаем API и бота в разных процессах
    api_process = multiprocessing.Process(target=run_api)
    bot_process = multiprocessing.Process(target=bot_process_func)

    api_process.start()
    bot_process.start()

    api_process.join()
    bot_process.join()