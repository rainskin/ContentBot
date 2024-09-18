import asyncio

from core.ad_manager import ad_manager

async def start():
    asyncio.create_task(ad_manager.run_check_ads_task())

