import asyncio

from core.ad_manager import ad_manager

tasks = []
async def start():

    task = asyncio.create_task(ad_manager.run_check_ads_task())
    tasks.append(task)

