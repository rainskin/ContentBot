from aiogram import types
from aiogram.dispatcher import FSMContext

import config
import texts
from loader import bot, dp
from states import States


@dp.callback_query_handler(state=States.schedule)
async def chose_category(callback_query: types.CallbackQuery, state: FSMContext):
    chat = callback_query.data
    channel_name = ''
    chat_id = ''
    if chat == 'anime_tyan':
        channel_name = 'Аниме тянки'
        chat_id = config.ANIME_CHAN_ID

    elif chat == 'yuri':
        channel_name = 'Юри'
        chat_id = config.YURI_ID

    elif chat == 'cute_pics':
        channel_name = 'Пикчи для диалогов'
        chat_id = config.CUTE_PICS_ID

    await state.update_data({'chat': chat, 'chat_id': chat_id})
    await bot.send_message(callback_query.message.chat.id, f'Ты выбрал канал *{channel_name}*',
                           parse_mode=types.ParseMode.MARKDOWN)
    await bot.send_message(callback_query.message.chat.id, text=texts.choosing_days,
                           parse_mode=types.ParseMode.MARKDOWN)
    await States.choosing_days.set()
