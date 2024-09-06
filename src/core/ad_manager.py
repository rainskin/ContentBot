import asyncio
from datetime import datetime, timedelta, tzinfo, timezone
from typing import List

import config
import loader

tasks = set()


class AdManager:

    def __init__(self):
        self.client = loader.ad_manager_db_client

        self.db = self.client[config.MONGO_DB_NAME]
        self.published_posts = self.db['published_posts']
        self.sales = self.db['sales']
        self.bot = loader.bot

    async def create_unique_sale_time_idx(self):
        await self.published_posts.create_index(
            [('sale_msg_id', 1), ('time', 1)],
            unique=True,
            name='unique_sale_time_idx'
        )

    async def setup(self):
        await self.create_unique_sale_time_idx()
    def get_all_ads(self):
        return self.published_posts.find()

    async def create_deletion_task(self, from_chat: int, msg_id: int, sale_msg_id: int, post_time: str,
                                   autodelete_timer: int):
        """Ставим таймер на удаление. Т.е. создаем задачу"""
        current_date = datetime.now()
        deletion_date = current_date + timedelta(seconds=autodelete_timer)

        asyncio.create_task(self.schedule_deletion(from_chat, msg_id, deletion_date, sale_msg_id, post_time))

    async def check_old_published_ads_and_delete(self):
        # sec = 36000  # seconds between checks
        sec = 60  # seconds between checks
        while True:

            all_ads = self.get_all_ads()

            async for ad in all_ads:
                deletion_date = ad.get('deletion_date')
                current_datetime = datetime.now()
                if current_datetime > deletion_date:
                    sale_msg_id = ad.get('sale_msg_id')
                    post_time = ad.get('time')
                    for chat_id, message_ids in ad['published_posts'].items():
                        for message_id in message_ids:
                            await self.delete_post(chat_id, message_id, sale_msg_id, post_time)

                        await self.delete_from_published_sales(sale_msg_id, post_time)

            await asyncio.sleep(sec)

    async def delete_post(self, from_chat, msg_id, sale_msg_id, post_time):
        await self.bot.delete_message(from_chat, msg_id)
        await self.delete_from_published_posts(from_chat, msg_id, sale_msg_id, post_time)

    async def schedule_deletion(self, from_chat: int, msg_id: int, deletion_date: datetime, sale_msg_id: int,
                                post_time: str):
        sec = 1  # seconds between checks
        while True:
            current_date = datetime.now()

            if current_date >= deletion_date:
                await self.bot.delete_message(from_chat, msg_id)
                await self.delete_from_published_posts(from_chat, msg_id, sale_msg_id, post_time)
                break
            else:
                await asyncio.sleep(sec)

    async def register_published_ad(self, sale_msg_id: int, time: str, autodelete_timer: int):

        if await self.sale_is_published(sale_msg_id, time):
            return

        sale = await self.sales.find_one({'sale_msg_id': sale_msg_id, 'time': time})
        title = sale.get('title')

        doc = {'sale_msg_id': sale_msg_id,
               'title': title,
               'time': time,
               'published_posts': dict(),
               'autodelete_timer': autodelete_timer,
               }

        if autodelete_timer:
            deletion_date = datetime.now() + timedelta(seconds=autodelete_timer)
            doc['deletion_date'] = deletion_date

        await self.published_posts.insert_one(doc)

    async def sale_is_published(self, sale_msg_id: int, time: str) -> bool:
        doc = await self.published_posts.find_one({'sale_msg_id': sale_msg_id, 'time': time})
        r = doc is not None
        return r

    async def post_is_published(self, sale_msg_id: int, time: str, chat_id: int, msg_id: int):
        doc = await self.published_posts.find_one({'sale_msg_id': sale_msg_id, 'time': time})

        if not doc:
            return False

        published_posts: dict = doc.get('published_posts')

        if published_posts:
            return msg_id in published_posts.get(chat_id, [])

        return False

    async def add_to_published_posts(self, sale_msg_id: int, time: str, chat_id: int, msg_ids: List[int]):

        await self.published_posts.find_one_and_update(
            {'sale_msg_id': sale_msg_id, 'time': time},
            {'$addToSet': {f'published_posts.{chat_id}': {'$each': msg_ids}}},
            upsert=True
        )

    async def delete_from_published_posts(self, from_chat: int, msg_id: int, sale_msg_id: int, time: str):
        await self.published_posts.update_one({'sale_msg_id': sale_msg_id, 'time': time},
                                              {'$pull': {f'published_posts.{from_chat}': msg_id}})

    async def delete_from_published_sales(self, sale_msg_id, post_time):
        await self.published_posts.delete_one({'sale_msg_id': sale_msg_id, 'time': post_time})


ad_manager = AdManager()