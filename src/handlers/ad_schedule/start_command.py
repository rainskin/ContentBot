from aiogram import types
from aiogram.dispatcher import FSMContext

import keyboards
import texts
from config import UPLOAD_CHANNEL_ID
from loader import dp, list_of_admins
from states import States
from utils.check_admin_rights import is_superadmin, is_admin


@dp.message_handler(commands='ad_schedule')
async def _(msg: types.Message, state: FSMContext):
    if not is_admin(msg.from_user.id):
        await msg.answer('Нет доступа')
        return

    if msg.chat.id != UPLOAD_CHANNEL_ID:
        await msg.answer(texts.schedule_start_command, disable_web_page_preview=True)
        return


    await States.get_channels_for_ad.set()
    await msg.answer(
        f'Отправь список каналов, в которые хочешь запланировать пост')

