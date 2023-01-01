from aiogram import types

import keyboards
import texts
from loader import dp
from states import States


@dp.message_handler(commands='schedule')
async def cmd_schedule(msg: types.Message):
    if msg.from_user.id != 936845322:
        await msg.answer('Нет доступа')
    else:
        await msg.answer(text=texts.schedule_main, reply_markup=keyboards.channels_kb)
        await States.schedule.set()
