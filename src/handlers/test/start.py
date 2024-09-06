from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType

import keyboards
from loader import dp, bot, userbot
from states import States
from utils.check_admin_rights import is_superadmin
from utils.time import get_current_datetime


@dp.message_handler(commands='test')
async def cmd_test(msg: types.Message, state: FSMContext):
    if not is_superadmin(msg.from_user.id):
        return

    await msg.answer('test', reply_markup=keyboards.test_kb)


@dp.message_handler(state=States.test, content_types=ContentType.ANY)
async def _(msg: types.Message, state: FSMContext):
    print(msg)
