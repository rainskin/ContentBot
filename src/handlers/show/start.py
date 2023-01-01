from aiogram import types

import keyboards
from loader import dp
from states import States


@dp.message_handler(commands='show')
async def cmd_show(msg: types.Message):
    if msg.from_user.id != 936845322:
        await msg.answer('Нет доступа')
    else:
        await msg.answer('Выбери категорию', reply_markup=keyboards.category_kb)
        await States.choosing_category.set()
