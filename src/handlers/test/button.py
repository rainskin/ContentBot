from aiogram import types

from loader import dp, bot


@dp.callback_query_handler(text='test_btn')
async def delete_photo(query: types.CallbackQuery):
    await query.message.answer('борозда')
