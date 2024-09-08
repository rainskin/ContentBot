import asyncio

from aiogram import executor

import background_tasks
import handlers
from core.ad_manager import ad_manager
from loader import dp
from utils.debug import check_memory_usage, check_task_amount

handlers.setup()


async def on_startup(dp):
    # Запуск фоновой задачи для проверки памяти
    asyncio.create_task(check_memory_usage(300))
    asyncio.create_task(check_task_amount(300))

    # Запуск фоновых задач бота
    await background_tasks.start()
    await ad_manager.setup()

    print('Задачи запущены')


# Запуск бота
executor.start_polling(dp, skip_updates=True, on_startup=on_startup)