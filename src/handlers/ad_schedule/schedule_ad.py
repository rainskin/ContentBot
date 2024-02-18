import asyncio
from datetime import datetime
from typing import Iterable

from aiogram import types
from aiogram.dispatcher import FSMContext

import config
import keyboards
from loader import dp, userbot, sales, bot
from states import States
from utils import db
from utils.time import create_valid_date


@dp.callback_query_handler(text='start_schedule', state=States.schedule_ad)
async def _(query: types.CallbackQuery, state: FSMContext):
    await query.message.edit_reply_markup(None)

    data = await state.get_data()
    sale_msg_id = data['sale_msg_id']
    ad_title_msg_id = data['ad_title_msg_id']
    ad_title_text = str(data['ad_title_text'])
    ad_title_text = ad_title_text.replace('принят', '\n\n✅ <b>Запланирован</b>')
    sale_data = sales.find_one({'sale_msg_id': sale_msg_id})
    date = sale_data['date'].split('-')
    year = int(date[2])
    month = int(date[1])
    day = int(date[0])
    # day = data['day']
    time = sale_data['time'].split(':')
    hour = int(time[0])
    minutes = int(time[1])
    channel_ids = sale_data['channel_ids']
    link = data['link']
    title = data['title']
    msg_id = data['message_id']
    drop_author = not data['drop_author']
    notification = not data['notification']

    schedule_date = datetime(year, month, day, hour, minutes)

    service_msg = await query.message.answer('...Начинаю планирование')

    scheduled_posts = []
    for channel_id in channel_ids:
        scheduled_msg = await userbot.forward_messages(channel_id, config.SALE_GROUP_ID, msg_id, schedule_date=schedule_date,
                                                       drop_author=drop_author, disable_notification=notification)
        scheduled_posts.append(scheduled_msg)

    await db.add_ad_post_info(sale_msg_id, title, link, scheduled_posts)

    await bot.edit_message_reply_markup(query.message.chat.id, sale_msg_id,
                                        reply_markup=keyboards.SaleSettings(sale_info=await db.sale_info_is_exist(sale_msg_id), ad_is_scheduled=True))
    await state.finish()
    await delete_messages(query.message.chat.id, service_msg.message_id)
    await bot.edit_message_text(ad_title_text, query.message.chat.id, ad_title_msg_id, parse_mode='html', disable_web_page_preview=True)
    await asyncio.sleep(5)
    await delete_messages(query.message.chat.id, msg_id)


@dp.callback_query_handler(text='cancel', state=States.schedule_ad)
async def _(query: types.CallbackQuery, state: FSMContext):
    await query.answer('Действие отменено')
    await state.finish()
    await query.message.delete()


async def delete_messages(chat_id: int, message_ids: int | Iterable[int]):
    is_iterable = not isinstance(message_ids, int)
    message_ids = list(message_ids) if is_iterable else [message_ids]

    for message_id in message_ids:
        await bot.delete_message(chat_id, message_id)
