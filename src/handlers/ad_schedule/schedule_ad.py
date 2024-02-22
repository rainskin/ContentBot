import asyncio
from datetime import timedelta
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
    is_album = data['is_album']
    is_main_post = data['is_main_post']
    link = data['link']  # !!!!

    sale_msg_id = data['sale_msg_id']
    minute = data['minute'] if 'minute' in data else 0
    ad_title_msg_id = data['ad_title_msg_id']
    ad_title_text = str(data['ad_title_text'])

    sale_data = sales.find_one({'sale_msg_id': sale_msg_id})

    channel_ids = sale_data['channel_ids']
    title = data['title']

    msg_ids_in_data = data['message_id']
    drop_author = not data['drop_author']
    notification = not data['notification']
    notification_status_in_text = '🔕 Без звука' if notification else '🔔 Со звуком'
    drop_author_status_in_text = '🚷 Без автора' if drop_author else '👤 Репост'

    schedule_date = await db.get_scheduled_post_datetime(sale_msg_id)
    schedule_date = schedule_date if is_main_post else schedule_date + timedelta(minutes=minute)

    ad_title_text = ad_title_text.replace('принят',
                                          f'\n\n✅ <b>Запланирован</b>\n<i>{notification_status_in_text} | {drop_author_status_in_text}</i>')
    msg_id = await userbot.get_msg_ids(query.message.chat.id, msg_ids_in_data[0]) if is_album else msg_ids_in_data
    service_msg = await query.message.answer('...Начинаю планирование')

    scheduled_posts = []
    for channel_id in channel_ids:
        scheduled_messages = await userbot.forward_messages(channel_id, config.SALE_GROUP_ID, msg_id,
                                                            schedule_date=schedule_date,
                                                            drop_author=drop_author, disable_notification=notification)

        scheduled_posts += scheduled_messages

    if is_main_post:
        await db.add_ad_post_info(sale_msg_id, title, link, scheduled_posts)
        sale_info = await db.sale_info_is_exist(sale_msg_id)
        await bot.edit_message_reply_markup(query.message.chat.id, sale_msg_id,
                                            reply_markup=keyboards.SaleSettings(sale_info=sale_info,
                                                                                ad_is_scheduled=True))
    else:
        await db.add_ad_additional_posts(sale_msg_id, scheduled_posts)
        # service_msg_id = data['service_msg_id']

    await bot.delete_message(query.message.chat.id, service_msg.message_id)
    await state.finish()
    await delete_messages(query.message.chat.id, msg_id)
    await bot.edit_message_text(ad_title_text, query.message.chat.id, ad_title_msg_id, parse_mode='html',
                                disable_web_page_preview=True)


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
