from datetime import datetime

from aiogram import types

from loader import dp
from utils.check_admin_rights import is_superadmin


@dp.message_handler(commands='test')
async def cmd_test(msg: types.Message):
    if not is_superadmin(msg.from_user.id):
        return


