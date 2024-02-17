from aiogram import types

import keyboards
from loader import dp, bot, userbot
from utils.check_admin_rights import is_admin, is_superadmin


@dp.message_handler(commands='test')
async def cmd_test(msg: types.Message):
    if not is_superadmin(msg.from_user.id):
        return
