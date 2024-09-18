import asyncio
from pyrogram_patch import patch_pyrogram
from aiogram import executor

import background_tasks
import handlers
from core.ad_manager import ad_manager
from loader import dp, bot
from utils.debug import check_memory_usage, check_task_amount

patch_pyrogram()
handlers.setup()


async def on_startup(dp):
    # Запуск фоновой задачи для проверки памяти
    asyncio.create_task(check_memory_usage(60*60))
    asyncio.create_task(check_task_amount(60*60))

    # Запуск фоновых задач бота
    await background_tasks.start()
    await ad_manager.setup()
    await bot.delete_webhook()

    print('Задачи запущены')

executor.start_polling(dp, skip_updates=True, on_startup=on_startup, allowed_updates=[])
