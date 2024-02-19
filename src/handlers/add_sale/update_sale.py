from aiogram import types
from aiogram.dispatcher import FSMContext

from config import SALE_GROUP_ID
from loader import dp


@dp.callback_query_handler(text='add_sale_info', state=None)
async def _(query: types.CallbackQuery, state: FSMContext):
    if query.message.chat.id != SALE_GROUP_ID:
        return
    await query.answer('Это функция пока недоступна')


@dp.callback_query_handler(text='update_sale_info', state=None)
async def _(query: types.CallbackQuery):
    if query.message.chat.id != SALE_GROUP_ID:
        return
    await query.answer('Это функция пока недоступна')
