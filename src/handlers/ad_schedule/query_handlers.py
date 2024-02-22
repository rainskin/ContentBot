from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext

import keyboards
from config import SALE_GROUP_ID
from loader import dp, userbot
from states import States
from utils import db
from utils.time import create_valid_date


@dp.callback_query_handler(text='schedule_ad_post', state=None)
async def _(query: types.CallbackQuery, state: FSMContext):
    if query.message.chat.id != SALE_GROUP_ID:
        return

    await query.answer()
    await query.message.edit_reply_markup(None)
    service_msg = await query.message.answer('Теперь отправь рекламный пост')
    await state.update_data(sale_msg_id=query.message.message_id, service_msg_id=service_msg.message_id)
    await States.waiting_ad_post.set()


@dp.callback_query_handler(text='schedule_additional_ad_post', state=None)
async def _(query: types.CallbackQuery, state: FSMContext):
    if query.message.chat.id != SALE_GROUP_ID:
        return
    await query.answer('Это функция пока недоступна')


@dp.callback_query_handler(text='delete_scheduled_posts', state=None)
async def _(query: types.CallbackQuery, state: FSMContext):
    if query.message.chat.id != SALE_GROUP_ID:
        return
    sale_msg_id = query.message.message_id
    sale_info = await db.sale_info_is_exist(sale_msg_id)

    chats_and_messages = await db.get_scheduled_posts_info(sale_msg_id)
    count = 0
    for chat_id, msg_ids in chats_and_messages:
        await userbot.delete_scheduled_messages(chat_id, msg_ids)
        count += 1

    if count == len(chats_and_messages):
        await query.message.edit_reply_markup(keyboards.SaleSettings(sale_info=sale_info))
        await db.delete_scheduled_posts_info(query.message.message_id)
