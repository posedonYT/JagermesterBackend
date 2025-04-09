import uvicorn
import asyncio
from bot import dp, bot
from api import app
import multiprocessing
import signal
import sys

def run_api():
    uvicorn.run(app, host='176.113.82.88', port=8000)


async def run_bot():
    # Запуск бота
    await dp.start_polling(bot)


def bot_process_func():
    asyncio.run(run_bot())

def signal_handler(sig, frame):
    print("\nЗавершение процессов...")
    api_process.terminate()
    bot_process.terminate()
    sys.exit(0)


if __name__ == "__main__":
    # Запускаем API и бота в разных процессах
    api_process = multiprocessing.Process(target=run_api)
    bot_process = multiprocessing.Process(target=bot_process_func)

    api_process.start()
    bot_process.start()

    signal.signal(signal.SIGINT, signal_handler)

    try:
        api_process.join()
        bot_process.join()
    except KeyboardInterrupt:
        print("\nПрерывание пользователем")
        api_process.terminate()
        bot_process.terminate()