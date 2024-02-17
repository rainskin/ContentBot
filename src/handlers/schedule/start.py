from aiogram import types

import keyboards
import texts
from loader import dp
from states import States
from utils.check_admin_rights import is_admin, is_superadmin


@dp.message_handler(commands='schedule')
async def cmd_schedule(msg: types.Message):
    if not is_superadmin(msg.from_user.id):
        return
    else:
        await msg.answer(text=texts.schedule_main, reply_markup=keyboards.Channels())
        await States.schedule.set()
