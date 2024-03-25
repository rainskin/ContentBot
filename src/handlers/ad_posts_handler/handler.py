import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext

import config
import keyboards
from loader import dp, userbot, bot
from states import States
from utils import links
from utils.db import get_ids_of_all_channels


# @dp.message_handler(content_types="any")
# async def _(msg: types.Message, state: FSMContext):
#     if msg.chat.id not in get_ids_of_all_channels():
#         return
#     #
#     # current_date = get_current_datetime()
#     # if