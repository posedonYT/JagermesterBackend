import uvicorn
import asyncio
from bot import dp, bot
from api import app
import multiprocessing
import signal
import sys
import os
import time


def run_api():
    uvicorn.run(app, host='176.113.82.88', port=8000)


async def run_bot():
    await dp.start_polling(bot)
    await bot.session.close()  # Явное закрытие сессии


def bot_process_func():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(run_bot())
    finally:
        loop.close()


def signal_handler(sig, frame):
    print("\nЗавершение процессов...")

    # Отправляем SIGTERM дочерним процессам
    api_process.terminate()
    bot_process.terminate()

    # Дожидаемся завершения
    api_process.join()
    bot_process.join()

    # Гарантированно убиваем процессы если зависли
    if api_process.is_alive():
        api_process.kill()
    if bot_process.is_alive():
        bot_process.kill()

    sys.exit(0)


if __name__ == "__main__":
    api_process = multiprocessing.Process(target=run_api)
    bot_process = multiprocessing.Process(target=bot_process_func)

    api_process.start()
    bot_process.start()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        while True:
            # Проверяем статус процессов
            if not api_process.is_alive() or not bot_process.is_alive():
                break
            time.sleep(1)
    except KeyboardInterrupt:
        signal_handler(signal.SIGINT, None)