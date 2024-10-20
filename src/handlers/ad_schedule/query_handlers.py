
from aiogram import types
from aiogram.dispatcher import FSMContext

import keyboards
from core.db import users
from loader import dp, userbot, bot
from states import States
from utils import db
from utils.check_admin_rights import is_salesman, is_admin
from utils.db import delete_additional_posts_by_sale_id


@dp.callback_query_handler(text='schedule_ad_post', state=None)
async def _(query: types.CallbackQuery, state: FSMContext):
    channel_owner_id = query.from_user.id
    sale_group_id = await users.get_sale_group_id(channel_owner_id)

    if not sale_group_id:
        return

    if query.message.chat.id != sale_group_id:
        return
    sale_msg_id = query.message.message_id

    if not is_salesman(query.from_user.first_name, sale_msg_id) and not is_admin(query.from_user.id):
        await query.answer('У тебя нет прав для удаления чужих продаж')
        return

    await query.answer()
    await query.message.edit_reply_markup(None)
    service_msg = await query.message.answer('Теперь отправь рекламный пост')
    await States.waiting_ad_post.set()
    await state.update_data(sale_msg_id=query.message.message_id, service_msg_id=service_msg.message_id, is_main_post=True)


@dp.callback_query_handler(text='schedule_additional_ad_post', state=None)
async def _(query: types.CallbackQuery, state: FSMContext):
    channel_owner_id = query.from_user.id
    sale_group_id = await users.get_sale_group_id(channel_owner_id)
    if query.message.chat.id != sale_group_id:
        return
    sale_msg_id = query.message.message_id

    if not is_salesman(query.from_user.first_name, sale_msg_id) and not is_admin(query.from_user.id):
        await query.answer('У тебя нет прав для удаления чужих продаж')
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
    channel_owner_id = query.from_user.id
    sale_group_id = await users.get_sale_group_id(channel_owner_id)
    if query.message.chat.id != sale_group_id:
        return
    sale_msg_id = query.message.message_id
    channel_owner_id = query.from_user.id

    if not is_salesman(query.from_user.first_name, sale_msg_id) and not is_admin(query.from_user.id):
        # TODO replace is_admin checking on is_channel_owner check
        await query.answer('У тебя нет прав для управления чужими продажами')
        return

    sale_info = await db.is_sale_info_exist(channel_owner_id, sale_msg_id)

    chats_and_messages = await db.get_scheduled_posts(channel_owner_id, sale_msg_id)
    count = 0
    for chat_id, msg_ids in chats_and_messages:
        await userbot.delete_scheduled_messages(chat_id, msg_ids)
        count += 1

    if count == len(chats_and_messages):
        await query.message.edit_reply_markup(keyboards.SaleSettings(sale_info=sale_info))
        await db.delete_scheduled_posts_info(channel_owner_id, query.message.message_id)
        await delete_additional_posts_by_sale_id(channel_owner_id, sale_msg_id)
        await query.answer()
