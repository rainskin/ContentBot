from datetime import datetime, timedelta
from typing import List

import config
import loader


class Sales:

    def __init__(self):
        self.client = loader.ad_manager_db_client
        self.db = self.client[config.MONGO_DB_NAME]
        self.col = self.db['sales']
        self.default_datetime_format = '%d-%m-%Y %H:%M'
        self.date_format = '%d-%m-%Y'

    @staticmethod
    def format_date(date: datetime):
        day, month, year = date.day, date.month, date.year
        return '{}-{}-{}'.format(day, month, year)

    async def get_sales_for_specified_date(self, dt: datetime):
        day, month, year = dt.day, dt.month, dt.year
        date: str = '{}-{}-{}'.format(str(day), str(month), str(year))
        sales = self.col.find({'date': date})
        r = [sale async for sale in sales]
        return r

    async def get_closer_sale_id(self, post_datatime: datetime):

        today_sales = await self.get_sales_for_specified_date(datetime.now())
        yesterday_sales = await self.get_sales_for_specified_date(datetime.now() - timedelta(days=1))
        tomorrow_sales = await self.get_sales_for_specified_date(datetime.now() + timedelta(days=1))

        closer_sales = yesterday_sales + today_sales + tomorrow_sales
        difference = float('inf')
        _id = None
        for doc in closer_sales:
            # doc = await self.col.find_one({'_id': sale_id})
            sale_id = doc['_id']
            date = doc.get('date')
            time = doc.get('time')
            sale_date = datetime.strptime(f'{date} {time}', self.default_datetime_format)

            time_difference: float = abs((post_datatime - sale_date).total_seconds())

            if time_difference < difference:
                difference = time_difference
                _id = sale_id

        return _id

    async def get_closest_sales(self, post_datatime: datetime, time_period_in_minutes: int) -> list:
        time_period_in_seconds = time_period_in_minutes * 60
        today_sales = await self.get_sales_for_specified_date(datetime.now())
        yesterday_sales = await self.get_sales_for_specified_date(datetime.now() - timedelta(days=1))
        tomorrow_sales = await self.get_sales_for_specified_date(datetime.now() + timedelta(days=1))

        closer_sales = yesterday_sales + today_sales + tomorrow_sales
        closest_sales = []
        for doc in closer_sales:
            date = doc.get('date')
            time = doc.get('time')
            sale_date = datetime.strptime(f'{date} {time}', self.default_datetime_format)
            time_difference: float = abs((post_datatime - sale_date).total_seconds())
            if 0 <= time_difference <= time_period_in_seconds:
                closest_sales.append(doc)

        return closest_sales

    async def is_ad_post(self, chat_id: int, post_datatime: datetime) -> bool:
        # post_datatime = datetime(year=2024, month=4, day=1, hour=15, minute=21)
        str_date = self.format_date(post_datatime)

        today_sales = await self.get_sales_for_specified_date(datetime.now())

        difference = 0
        for sale in today_sales:
            time = sale['time']
            sale_date = datetime.strptime(f'{str_date} {time}', self.default_datetime_format)

            time_difference: float = (post_datatime - sale_date).total_seconds()

            if 0 < time_difference < 120 and chat_id in sale['channel_ids']:
                difference = time_difference
            else:
                continue

        return 0 < difference < 120

    async def get_autodelete_time(self, _id):
        doc = await self.col.find_one({'_id': _id})
        return doc.get('autodelete_timer')

    async def get_scheduled_posts(self, _id):
        return self.col.find_one({'_id': _id})['scheduled_posts']

    async def get_sale_data(self, _id) -> List[str]:
        return await self.col.find_one({'_id': _id})

    async def get_all_sales_by_date_and_time(self, date: str, time: str) -> list:
        sales = self.col.find({'date': date, 'time': time})
        r = [sale async for sale in sales]
        return r

    async def get_msg_markers(self, _id) -> List[str]:
        doc = await self.col.find_one({'_id': _id})
        return doc.get('markers')

    async def get_keyboard_data(self, _id) -> str:
        doc = await self.col.find_one({'_id': _id})
        return doc.get('keyboard_data')

    async def is_scheduled_post(self, _id):
        doc = await self.col.find_one({'_id': _id})
        return doc.get('scheduled_posts') is not None

    async def get_sale_msg_id_and_time_by_sale_id(self, _id):
        doc = await self.col.find_one({'_id': _id})
        return doc.get('sale_msg_id'), doc.get('time')

    # def is_ad_post(self, post_datatime: datetime):
    #     closer_sale = self.get_closer_sale_msg_id(post_datatime)
    #     msg_id = closer_sale[0]
    #     time_difference = closer_sale[1]
    #     sale = self.db.find_one({'sale_msg_id': msg_id})
    #
    #     if time_difference < -600:
    #         return
