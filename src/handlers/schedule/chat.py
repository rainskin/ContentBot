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

    elif chat == 'avatars':
        channel_name = 'Крутые авы'
        chat_id = config.AVATARS_ID

    elif chat == 'bubblekum':
        channel_name = 'Баблкам'
        chat_id = config.BUBBLEKUM_ID

    elif chat == 'irl_characters':
        channel_name = 'Вымышленные персонажи'
        chat_id = config.IRL_ID

    elif chat == 'zxc':
        channel_name = 'ZXC Авы'
        chat_id = config.ZXC_ID

    elif chat == 'hentai':
        channel_name = 'Хентай'
        chat_id = config.HENTAI_ID

    await state.update_data({'chat': chat, 'chat_id': chat_id})
    await bot.send_message(callback_query.message.chat.id, f'Ты выбрал канал *{channel_name}*',
                           parse_mode=types.ParseMode.MARKDOWN)
    await bot.send_message(callback_query.message.chat.id, text=texts.choosing_days,
                           parse_mode=types.ParseMode.MARKDOWN)
    await States.choosing_days.set()
