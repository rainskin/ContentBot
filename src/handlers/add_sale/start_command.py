from aiogram import types

import config
import texts
from config import SALE_GROUP_ID
from core.db import users
from loader import dp
from states import States
from utils.check_admin_rights import is_admin


@dp.message_handler(commands='add_sale')
async def _(msg: types.Message):
    if not is_admin(msg.from_user.id):
        await msg.answer('Нет доступа')
        return

    channel_owner_id = msg.from_user.id
    sale_group_id = await users.get_sale_group_id(channel_owner_id)

    if not sale_group_id:
        return

    if msg.chat.id != sale_group_id:
        await msg.answer('Это пока недоступно здесь', disable_web_page_preview=True)
        return

    await States.get_channels_for_ad.set()
    await msg.answer(f'Добавим продажу? Отправь сюда список каналов')
