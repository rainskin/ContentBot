import tracemalloc
import logging
import asyncio

# Включаем отслеживание потребления памяти
tracemalloc.start()

# Пример логирования
logging.basicConfig(level=logging.INFO)


async def check_memory_usage(timeout_seconds):
    while True:
        # Делаем снимок
        snapshot = tracemalloc.take_snapshot()
        top_stats = snapshot.statistics('lineno')

        logging.info("[ Топ 5 потребления памяти ]")
        for index, stat in enumerate(top_stats[:5], 1):
            logging.info(f"{index}. {stat.traceback.format()}: {stat.size / 1024:.1f} KiB")

        # Проверяем каждые 5 минут
        await asyncio.sleep(timeout_seconds)


async def check_task_amount(timeout_seconds: int):
    while True:
        all_tasks = asyncio.all_tasks()
        logging.info(f"Количество активных задач: {len(asyncio.all_tasks())}")
        for task in all_tasks:
            logging.info(f'{task}')
        await asyncio.sleep(timeout_seconds)
