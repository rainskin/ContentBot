import asyncio

from core.ad_manager import ad_manager


async def start():
    asyncio.create_task(ad_manager.check_old_published_ads_and_delete())
