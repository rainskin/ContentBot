import asyncio

from aiogram import types
from aiogram.utils.exceptions import WrongFileIdentifier

import keyboards
import lib
from loader import dp, bot


@dp.callback_query_handler(text='ConfirmParsing.button')
async def _(query: types.CallbackQuery):
    await query.message.edit_text('Начинаю парсить...')
    pictures = await lib.pictures.get_new()
    processed_pictures = []

    for i in pictures:
        try:
            await bot.send_photo(query.message.chat.id, photo=i, caption=i, reply_markup=keyboards.photo_kb)
        except WrongFileIdentifier:
            await query.message.answer(f'Я обосрался {i}')
        else:
            processed_pictures.append(i)
        await asyncio.sleep(0.1)

    lib.pictures.save(processed_pictures)
    await bot.send_message(query.message.chat.id, f'Количество новых пикч: {len(processed_pictures)}')
