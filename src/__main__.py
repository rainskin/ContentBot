from aiogram import executor

import background_tasks
import handlers
from core.ad_manager import ad_manager
from loader import dp

handlers.setup()


async def on_startup(dp):
    await background_tasks.start()
    await ad_manager.setup()
    print('Задачи запущены')


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
