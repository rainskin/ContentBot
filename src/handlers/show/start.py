from aiogram import types

import keyboards
from loader import dp
from states import States


@dp.message_handler(commands='show')
async def cmd_show(message: types.Message):
    await message.answer('Выбери категорию', reply_markup=keyboards.category_kb)
    await States.choosing_category.set()
