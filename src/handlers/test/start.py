from datetime import datetime

from aiogram import types

from loader import dp
from utils.check_admin_rights import is_superadmin


@dp.message_handler(commands='test')
async def cmd_test(msg: types.Message):
    if not is_superadmin(msg.from_user.id):
        return

    current_datetime = get_current_datetime()


def get_current_datetime():
    c_datetime = datetime.now()

    return {
        'hour': c_datetime.hour,
        'day': c_datetime.day,
        'month': c_datetime.month,
        'year': c_datetime.year,
        'time': str(c_datetime.minute) + ':' + str(c_datetime.second)
    }


