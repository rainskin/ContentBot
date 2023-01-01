from aiogram import types
from aiogram.dispatcher import FSMContext

import config
import keyboards
from loader import dp, bot
from states import States


@dp.message_handler(commands='upload', state='*')
async def cmd_upload(msg: types.Message, state: FSMContext):
    if msg.from_user.id != 936845322:
        await msg.answer('Нет доступа')
    else:
        if msg.from_user.id != 936845322:
            await msg.answer('Нет доступа')
        else:
            if msg.chat.id != -1001723603976:
                await msg.answer(f'Загружать контент нужно в специальном канале: {config.UPLOAD_CHANNEL_LINK}')
            else:
                await state.finish()
                await bot.send_message(msg.chat.id, 'Выбери канал для загрузки контента', reply_markup=keyboards.channels_kb)
                await States.upload_channel.set()

