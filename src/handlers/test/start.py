from aiogram import types

import keyboards
from loader import dp, bot


@dp.message_handler(commands='test')
async def cmd_test(message: types.Message):
    await message.answer('Тестируемся')
    photo = 'https://preview.redd.it/0ju4n3ksqd3a1.png?width=640&crop=smart&auto=webp&s=069777ae65849d2a1cefd4bc6b5e9529a3cb4a9c'
    msg = await bot.send_photo(message.chat.id, photo=photo, reply_markup=keyboards.test_kb)
    print(msg)
    print(msg.photo[-1].file_id)
