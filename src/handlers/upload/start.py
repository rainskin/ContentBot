from aiogram import types
from aiogram.dispatcher import FSMContext

import keyboards
import texts
from config import UPLOAD_CHANNEL_ID
from loader import dp, bot
from states import States
from utils.check_admin_rights import is_superadmin


@dp.message_handler(commands='upload', state='*')
async def cmd_upload(msg: types.Message, state: FSMContext):
    if not is_superadmin(msg.from_user.id):
        return

    if msg.chat.id != UPLOAD_CHANNEL_ID:
        await msg.answer(texts.schedule_start_command, disable_web_page_preview=True)
        return

    await state.finish()

    await bot.send_message(msg.chat.id, 'Выбери канал для загрузки контента', reply_markup=keyboards.Channels())
    await States.upload_channel.set()


