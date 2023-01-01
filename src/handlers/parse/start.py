from aiogram import types

import keyboards
from loader import dp


@dp.message_handler(commands='parse')
async def _(msg: types.Message):
    if msg.from_user.id != 936845322:
        await msg.answer('Нет доступа')
    else:
        kb = keyboards.ConfirmParsing()
        await msg.answer('Начать?', reply_markup=kb)
