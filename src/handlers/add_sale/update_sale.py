from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext

from config import SALE_GROUP_ID
from loader import dp, userbot
from states import States
from utils import db
from utils.time import create_valid_date


@dp.callback_query_handler(text='add_sale_info', state=None)
async def _(query: types.CallbackQuery, state: FSMContext):
    if query.message.chat.id != SALE_GROUP_ID:
        return
    await query.answer('Это функция пока недоступна')


@dp.callback_query_handler(text='update_sale_info', state=None)
async def _(query: types.CallbackQuery, state: FSMContext):
    if query.message.chat.id != SALE_GROUP_ID:
        return
    await query.answer('Это функция пока недоступна')