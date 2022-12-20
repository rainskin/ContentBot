from aiogram import types

import keyboards
import texts
from loader import dp
from states import States


@dp.message_handler(commands='schedule')
async def cmd_schedule(message: types.Message):
    await message.answer(text=texts.schedule_main, reply_markup=keyboards.channels_kb)
    await States.schedule.set()
