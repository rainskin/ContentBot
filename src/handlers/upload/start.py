from aiogram import types
from aiogram.dispatcher import FSMContext

import keyboards
from loader import dp, bot
from states import States


@dp.message_handler(commands='upload', state='*')
async def cmd_upload(message: types.Message, state: FSMContext):
    await state.finish()
    await bot.send_message(message.chat.id, 'Выбери канал для загрузки контента', reply_markup=keyboards.channels_kb)
    await States.upload_channel.set()

