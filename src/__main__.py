from aiogram import executor

import background_tasks
import handlers
from core.ad_manager import ad_manager
from loader import dp

handlers.setup()


async def on_startup(dp):
    print("on_startup: Starting background tasks...")  # Лог перед стартом задач
    await background_tasks.start()
    print("on_startup: Background tasks started.")  # Лог после старта задач

    print("on_startup: Setting up ad manager...")  # Лог перед настройкой ad_manager
    await ad_manager.setup()
    print("on_startup: Ad manager setup complete.")  # Лог после настройки ad_manager

    print('on_startup: Задачи запущены')


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
