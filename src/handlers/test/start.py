from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp, bot, userbot
from states import States
from utils.check_admin_rights import is_superadmin
from utils.time import get_current_datetime


@dp.message_handler(commands='test')
async def cmd_test(msg: types.Message, state: FSMContext):
    if not is_superadmin(msg.from_user.id):
        return

    time = get_current_datetime()
    print(time['time'])
    # await States.test.set()

# @dp.message_handler(state=States.test)
# async def _(msg: types.Message, state: FSMContext):
#     await userbot.