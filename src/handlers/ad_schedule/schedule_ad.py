import asyncio
import datetime
from datetime import timedelta
from typing import Iterable

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import MessageToDeleteNotFound, MessageNotModified

import config
import keyboards
from core.db import channels
from handlers.add_sale.get_channels import get_channels_list_text
from loader import dp, userbot, sales, bot
from states import States
from utils import db
from utils.time import str_time_to_seconds, RU_MONTHS_GEN


@dp.callback_query_handler(text='start_schedule', state=States.schedule_ad)
async def _(query: types.CallbackQuery, state: FSMContext):
    await query.message.edit_reply_markup(None)

    channel_owner_id = query.from_user.id
    data = await state.get_data()
    is_album = data['is_album']
    is_main_post = data['is_main_post']

    sale_msg_id = data['sale_msg_id']
    minute = data['minute'] if 'minute' in data else 0
    ad_title_msg_id = data['ad_title_msg_id']
    ad_title_text = str(data['ad_title_text'])

    sale_data = sales.find_one({'sale_msg_id': sale_msg_id})
    channel_ids = sale_data['channel_ids']
    data['channel_ids'] = channel_ids
    chanel_titles = await channels.get_channels_titles_by_id(channel_owner_id, channel_ids)
    chanel_links = await channels.get_channel_links_by_id(channel_owner_id, channel_ids)
    from_chat_id = data.get('from_chat_id')
    service_msg_ids = data.get('service_msg_ids')
    msg_ids_in_data = data['message_id']
    drop_author = not data['drop_author']
    notification = not data['notification']
    autodelete_timer: str = data.get('autodelete_timer')
    keyboard_data = data.get('keyboard_data')
    if not drop_author and keyboard_data:
        data['keyboard_data'] = None


    notification_status_in_text = '🔕 Без звука' if notification else '🔔 Со звуком'
    drop_author_status_in_text = '🚷 Без автора' if drop_author else '👤 Репост'

    hours, minutes = autodelete_timer.split(':') if autodelete_timer else (0, 0)

    autodelete_timer_in_text = f'<i>🗑 Удалить через</i>: {hours} ч {minutes} мин' if autodelete_timer else '<i>🗑 Без удаления</i>'

    schedule_date = await db.get_scheduled_post_datetime(channel_owner_id, sale_msg_id)
    schedule_date = schedule_date if is_main_post else schedule_date + timedelta(minutes=minute)

    current_datetime = datetime.datetime.now()
    if datetime.datetime.now() >= schedule_date:
        schedule_date = current_datetime + timedelta(minutes=1)


    ad_title_text = ad_title_text.replace('принят',
                                          f'\n\n✅ <b>Запланирован</b>\n<i>{notification_status_in_text} | {drop_author_status_in_text}</i>\n'
                                          f'{autodelete_timer_in_text}')
    msg_id = await userbot.get_msg_ids(query.message.chat.id, msg_ids_in_data[0]) if is_album else msg_ids_in_data
    service_msg = await query.message.answer('...Начинаю планирование')

    scheduled_posts = []

    for channel_id in channel_ids:
        scheduled_messages = await userbot.forward_messages(channel_id, from_chat_id, msg_id,
                                                            schedule_date=schedule_date,
                                                            drop_author=drop_author, disable_notification=notification)

        scheduled_posts += scheduled_messages

    await update_scheduled_post_info(channel_owner_id, chanel_titles, is_main_post, data, schedule_date, scheduled_posts)

    if is_main_post:
        await update_sale_message_keyboard(query, channel_owner_id, sale_msg_id)

    await state.finish()

    if service_msg_ids:
        await delete_messages(query.message.chat.id, service_msg_ids)

    await delete_messages(query.message.chat.id, msg_id)
    await bot.edit_message_text(ad_title_text, query.message.chat.id, ad_title_msg_id,
                                disable_web_page_preview=True)

    await send_report_about_scheduled_posts(query.message.chat.id, chanel_titles, chanel_links, schedule_date, data)
    await bot.delete_message(query.message.chat.id, service_msg.message_id)


@dp.callback_query_handler(text='cancel',
                           state=[States.schedule_ad, States.take_inline_keyboard, States.take_autodelete_timer])

async def _(query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    sale_msg_id = data['sale_msg_id']
    channel_owner_id = data['channel_owner_id']
    sale_info = await db.is_sale_info_exist(channel_owner_id, sale_msg_id)
    ad_is_scheduled = await db.is_scheduled_posts_exist(channel_owner_id, sale_msg_id)
    try:
        await bot.edit_message_reply_markup(query.message.chat.id, sale_msg_id, reply_markup=keyboards.SaleSettings(sale_info, ad_is_scheduled))
    except MessageNotModified as e:
        pass

    await query.answer('Действие отменено')
    await state.finish()
    await query.message.delete()


async def delete_messages(chat_id: int, message_ids: int | Iterable[int]):
    is_iterable = not isinstance(message_ids, int)
    message_ids = list(message_ids) if is_iterable else [message_ids]

    for message_id in message_ids:
        try:
            await bot.delete_message(chat_id, message_id)
        except MessageToDeleteNotFound:
            pass


async def send_report_about_scheduled_posts(chat_id: int, chanel_titles: list[str], chanel_links: list[str], schedule_date: datetime, data: dict):
    text = await get_report_text_about_scheduled_posts(chanel_titles, chanel_links, schedule_date, data)
    await bot.send_message(chat_id, text, disable_web_page_preview=True)


async def get_report_text_about_scheduled_posts(channel_names: list[str], channel_links: list[str], schedule_date: datetime.datetime, data: dict) -> str:
    title = data.get('title')
    channel_ids = data.get('channel_ids')

    # channel_links = [await channels.get_channel_link_by_title(channel_owner, title) for title in channel_names]

    channel_list = get_channels_list_text(channel_names, channel_links)

    header = f'📋 Пост <b>«{title}»</b>'
    schedule_day = schedule_date.day
    schedule_month = schedule_date.month
    schedule_time = schedule_date.time()
    date = f'{schedule_day} {RU_MONTHS_GEN[schedule_month - 1]} {schedule_time.hour}:{schedule_time.minute:02d}'
    text = (f'{header}\n'
            f'Будет опубликован <b>{date}</b> в следующих каналах:\n\n'
            f'{channel_list}')

    return text


async def update_scheduled_post_info(channel_owner_id: int, chanel_titles: list[str], is_main_post: bool, data: dict, schedule_date: datetime, scheduled_posts: list):
    sale_msg_id = data['sale_msg_id']
    autodelete_timer: str = data.get('autodelete_timer')
    link = data['link']  # !!!!
    title = data['title']
    message_markers: list = data['message_markers']

    keyboard_data = data.get('keyboard_data')

    autodelete_time_in_sec = str_time_to_seconds(autodelete_timer) if autodelete_timer else None
    if is_main_post:
        await db.add_ad_post_info(channel_owner_id, sale_msg_id, title, link, keyboard_data, message_markers, scheduled_posts,
                                  autodelete_time_in_sec)
    else:
        await db.add_ad_additional_posts(channel_owner_id, sale_msg_id, schedule_date, chanel_titles, title, keyboard_data, message_markers,
                                         scheduled_posts, autodelete_time_in_sec)


async def update_sale_message_keyboard(query: types.CallbackQuery, channel_owner_id: int,  sale_msg_id: int):
    sale_info = await db.is_sale_info_exist(channel_owner_id, sale_msg_id)
    await bot.edit_message_reply_markup(query.message.chat.id, sale_msg_id,
                                        reply_markup=keyboards.SaleSettings(sale_info=sale_info,
                                                                            ad_is_scheduled=True))
