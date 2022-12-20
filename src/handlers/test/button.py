from aiogram import types

from loader import dp, bot


@dp.callback_query_handler(text='test_btn')
async def delete_photo(callback_query: types.CallbackQuery):
    text = callback_query.message.photo[-1].file_id
    await bot.send_message(callback_query.message.chat.id, text)
