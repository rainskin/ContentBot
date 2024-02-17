from aiogram import types

import keyboards
from loader import dp
from utils.check_admin_rights import is_superadmin


@dp.message_handler(commands='parse')
async def _(msg: types.Message):
    if not is_superadmin(msg.from_user.id):
        return

    kb = keyboards.ConfirmParsing()
    await msg.answer('Начать?', reply_markup=kb)
