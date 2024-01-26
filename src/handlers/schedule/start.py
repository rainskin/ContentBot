from aiogram import types

import keyboards
import texts
from loader import dp
from states import States
from utils.check_admin_rights import is_admin


@dp.message_handler(commands='schedule')
async def cmd_schedule(msg: types.Message):
    if not is_admin(msg.from_user.id):
        await msg.answer('Нет доступа')
    else:
        await msg.answer(text=texts.schedule_main, reply_markup=keyboards.Channels())
        await States.schedule.set()
