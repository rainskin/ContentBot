import asyncio
import datetime
import logging
import random
from datetime import datetime
from typing import List

import pyrogram.errors
from aiogram import types
from aiogram.utils.exceptions import RetryAfter
from bson import ObjectId
from pymongo.errors import DuplicateKeyError

from core.ad_manager import ad_manager
from core.db import sales

from keyboards import InlineKeyboardBuilder
from utils import db
from utils.media_group_collector import collect_media_group

from loader import dp, bot
from utils.msg_marker import get_marker


async def add_keyboard(chat_id: int, msg_id: int, closer_sale_id: ObjectId):
    keyboard_data = await sales.get_keyboard_data(closer_sale_id)
    print(keyboard_data, type(keyboard_data))

    if not keyboard_data:
        return

    kb = InlineKeyboardBuilder(keyboard_data)
    await asyncio.sleep(random.randint(1, 5))

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

    try:
        await add_keyboard(chat_id, messages[0].message_id, sale_id)
    except RetryAfter as e:
        await asyncio.sleep(e.timeout)
        await add_keyboard(chat_id, messages[0].message_id, sale_id)

    sale_msg_id, time = await sales.get_sale_msg_id_and_time_by_sale_id(sale_id)
    autodelete_time = await sales.get_autodelete_time(sale_id)

    if not autodelete_time:
        return

    if not await ad_manager.sale_is_published(sale_msg_id, time):
        try:
            await ad_manager.register_published_ad(sale_msg_id, time, autodelete_time)
        except DuplicateKeyError:
            pass

    await ad_manager.add_to_published_posts(sale_msg_id, time, chat_id, msg_ids)


@dp.channel_post_handler(content_types=types.ContentType.ANY)
async def func(msg: types.Message):
    messages = await collect_media_group(msg)
    chat_id = msg.chat.id

    if chat_id not in await ad_manager.get_ids_of_all_channels():
        return

    if not messages:
        return

    await asyncio.sleep((len(messages) * 2))  # waiting for all posts to come out

    logging.info(f'Начал обработку в {messages[0].chat.title}, кол-во сообщений {len(messages)}')
    date = messages[0].date

    closer_sale_id = await sales.get_closer_sale_id(date)

    if not closer_sale_id:
        return

    msg_date = messages[0].date
    closest_sales = await sales.get_closest_sales(msg_date, 30)

    for sale in closest_sales:
        asyncio.create_task(process_sale(chat_id, messages, sale))
        await asyncio.sleep(3)

    logging.info(f'Закончил обработку поста в {messages[0].chat.title}')
