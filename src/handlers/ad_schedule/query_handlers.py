from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext

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