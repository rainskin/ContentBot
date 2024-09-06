from aiogram import types

import config
import texts
from config import SALE_GROUP_ID
from loader import dp
from states import States
from utils.check_admin_rights import is_admin


@dp.message_handler(commands='add_sale')
async def _(msg: types.Message):
    if not is_admin(msg.from_user.id):
        await msg.answer('Нет доступа')
        return

    if msg.chat.id != SALE_GROUP_ID:
        await msg.answer('Это пока недоступно здесь', disable_web_page_preview=True)
        return

    await States.get_channels_for_ad.set()
    await msg.answer(f'Добавим продажу? Отправь сюда список каналов')
