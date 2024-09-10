import asyncio
import datetime
import logging
from datetime import datetime
from typing import List

from aiogram import types
from bson import ObjectId
from pymongo.errors import DuplicateKeyError

from core.ad_manager import ad_manager
from core.db import sales

from keyboards import InlineKeyboardBuilder
from utils import db
from utils.media_group_collector import collect_media_group

from loader import dp, bot
from utils.msg_marker import get_marker

MARKERS: dict[int, list[str]] = {}
MSGS_IDS: dict[int, list[int]] = {}


async def add_keyboard(chat_id: int, msg_id: int, closer_sale_id: ObjectId):
    keyboard_data = await sales.get_keyboard_data(closer_sale_id)
    if keyboard_data:
        kb = InlineKeyboardBuilder(keyboard_data)
        await bot.edit_message_reply_markup(chat_id, msg_id, reply_markup=kb)


async def is_same_markers(closer_sale_id: ObjectId, msg_markers: List[str]):
    closer_sale_msg_markers: list = await sales.get_msg_markers(closer_sale_id)

    return set(closer_sale_msg_markers) == set(msg_markers)


async def process_sale(chat_id: int, messages: list[types.Message], sale: dict):
    channel_ids = sale.get('channel_ids')

    if chat_id not in channel_ids:
        return

    if not messages:
        return

    sale_id = sale.get('_id')

    if not await sales.is_scheduled_post(sale_id):
        return

    markers = [get_marker(m) for m in messages]
    msg_ids = [m.message_id for m in messages]

    if not await is_same_markers(sale_id, markers):
        return

    sale_msg_id, time = await sales.get_sale_msg_id_and_time_by_sale_id(sale_id)
    autodelete_time = await sales.get_autodelete_time(sale_id)

    if not autodelete_time:
        return

    if not await ad_manager.sale_is_published(sale_msg_id, time):
        # if await ad_manager.post_is_published(sale_msg_id, time, chat_id, msg_ids):
        #     return
        try:
            await ad_manager.register_published_ad(sale_msg_id, time, autodelete_time)
        except DuplicateKeyError:
            return

    await add_keyboard(chat_id, messages[0].message_id, sale_id)
    await ad_manager.add_to_published_posts(sale_msg_id, time, chat_id, msg_ids)


async def process_message(chat_id, msg, sale):
    channel_ids = sale.get('channel_ids')

    if chat_id not in channel_ids:
        return

    if not msg:
        return

    sale_id = sale.get('_id')

    sale_msg_id, time = await sales.get_sale_msg_id_and_time_by_sale_id(sale_id)
    autodelete_time = await sales.get_autodelete_time(sale_id)

    if not autodelete_time:
        return

    if not await sales.is_scheduled_post(sale_id):
        return

    marker = get_marker(msg)

    markers = await sales.get_msg_markers(sale_id)
    if marker not in markers:
        return

    if not await ad_manager.sale_is_published(sale_msg_id, time):
        try:
            await ad_manager.register_published_ad(sale_msg_id, time, autodelete_time)
        except DuplicateKeyError:
            return

    if not msg.media_group_id:
        await add_keyboard(chat_id, msg.message_id, sale_id)

    await ad_manager.add_to_published_posts_one_message(sale_msg_id, time, chat_id, msg.message_id)
    logging.info(f'Задача должна была завершиться')


@dp.channel_post_handler(content_types=types.ContentType.ANY)
async def func(msg: types.Message):
    chat_id = msg.chat.id
    logging.info(f'фиксирую пост в {msg.chat.title}')

    if chat_id not in db.get_ids_of_all_channels():
        return

    # messages = await collect_media_group(msg)

    closer_sale_id = await sales.get_closer_sale_id(datetime.now())
    if not closer_sale_id:
        return

    sale_data = await sales.get_sale_data(closer_sale_id)
    date = sale_data.get('date')
    time = sale_data.get('time')

    sales_for_same_time = await sales.get_all_sales_by_date_and_time(date, time)

    for sale in sales_for_same_time:
        # asyncio.create_task(process_sale(chat_id, messages, sale))
        asyncio.create_task(process_message(chat_id, msg, sale))

    logging.info(f'Закончил обработку поста в {msg.chat.title}')
