from aiogram import types
from aiogram.dispatcher import FSMContext

import config
from loader import dp, bot
from states import States


@dp.callback_query_handler(state=States.upload_channel)
async def upload(callback_query: types.CallbackQuery, state: FSMContext):
    chat_name = callback_query.data
    channel_name = ''
    chat_id = ''

    if chat_name == 'anime_tyan':
        await bot.send_message(callback_query.message.chat.id,
                               'Контент для этого канала можешь загрузить через команду /parse')
        await state.finish()
        return

    elif chat_name == 'yuri':
        channel_name = 'Юри'
        chat_id = config.YURI_ID

    elif chat_name == 'cute_pics':
        channel_name = 'Пикчи для диалогов'
        chat_id = config.CUTE_PICS_ID

    await bot.send_message(callback_query.message.chat.id, f'Ты выбрал канал {channel_name}')
    await state.update_data(chat_name=chat_name, chat_id=chat_id)
    await bot.send_message(callback_query.message.chat.id, 'Отправляй сюда картинки, которые хочешь добавить в базу')
