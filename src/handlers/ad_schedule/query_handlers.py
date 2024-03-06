

from aiogram import types
from aiogram.dispatcher import FSMContext

import keyboards
from config import SALE_GROUP_ID
from loader import dp, userbot, bot
from states import States
from utils import db
from utils.check_admin_rights import is_salesman, is_admin
from utils.time import create_valid_date


@dp.callback_query_handler(text='schedule_ad_post', state=None)
async def _(query: types.CallbackQuery, state: FSMContext):
    if query.message.chat.id != SALE_GROUP_ID:
        return

    if not is_admin(query.from_user.id) or not is_salesman(query.from_user.first_name, query.message.message_id):
        await query.answer('У тебя нет прав для управления чужими продажами')
        return

    await query.answer()
    await query.message.edit_reply_markup(None)
    service_msg = await query.message.answer('Теперь отправь рекламный пост')
    await States.waiting_ad_post.set()
    await state.update_data(sale_msg_id=query.message.message_id, service_msg_id=service_msg.message_id, is_main_post=True)


@dp.callback_query_handler(text='schedule_additional_ad_post', state=None)
async def _(query: types.CallbackQuery, state: FSMContext):
    if query.message.chat.id != SALE_GROUP_ID:
        return

    if not is_admin(query.from_user.id) or not is_salesman(query.from_user.first_name, query.message.message_id):
        await query.answer('У тебя нет прав для управления чужими продажами')
        return

    service_msg = await query.message.answer('Через сколько минут запланировать следующий пост?')
    await States.add_additional_ad_post.set()
    await state.update_data(sale_msg_id=query.message.message_id, is_main_post=False, service_msg_id=service_msg.message_id)
    await query.answer()


@dp.message_handler(state=States.add_additional_ad_post)
async def _(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    service_msg_id = data['service_msg_id']
    try:
        minute = int(msg.text)
    except ValueError:
        await msg.answer('Что-то не так, попробуй еще раз')
        return

    if 0 < minute < 59:
        await bot.delete_message(msg.chat.id, service_msg_id)
        service_msg = await msg.answer('Теперь отправь рекламный пост')
        await state.update_data(service_msg_id=service_msg.message_id, minute=minute)
        await States.waiting_ad_post.set()
    else:
        await msg.answer('Ты указал неверное количество минут')
        return


@dp.callback_query_handler(text='delete_scheduled_posts', state=None)
async def _(query: types.CallbackQuery):
    if query.message.chat.id != SALE_GROUP_ID:
        return
    sale_msg_id = query.message.message_id

    if not is_salesman(query.from_user.first_name, sale_msg_id) and not is_admin(query.from_user.id):
        await query.answer('У тебя нет прав для управления чужими продажами')
        return

    sale_info = await db.sale_info_is_exist(sale_msg_id)

    chats_and_messages = await db.get_scheduled_posts(sale_msg_id)
    count = 0
    for chat_id, msg_ids in chats_and_messages:
        await userbot.delete_scheduled_messages(chat_id, msg_ids)
        count += 1

    if count == len(chats_and_messages):
        await query.message.edit_reply_markup(keyboards.SaleSettings(sale_info=sale_info))
        await db.delete_scheduled_posts_info(query.message.message_id)
        await query.answer()