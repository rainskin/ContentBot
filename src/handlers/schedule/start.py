from aiogram import types

import keyboards
import texts
from loader import dp, other_channels, list_of_channels
from states import States
from utils.check_admin_rights import is_admin, is_superadmin
from utils.db import get_ids_of_all_channels


@dp.message_handler(commands='schedule')
async def cmd_schedule(msg: types.Message):
    if not is_superadmin(msg.from_user.id):
        return
    else:
        # await count_posts_in_channels()

        await msg.answer(text=texts.schedule_main, reply_markup=keyboards.Channels())
        await States.schedule.set()


async def count_posts_in_channels():
    ids = get_ids_of_all_channels()
    r = []
    for _id in ids:
        title = other_channels.find_one({'channel_id': _id})['title']
        number_of_posts = other_channels.count_documents({'channel_id': _id})
        r.append((title, number_of_posts))

