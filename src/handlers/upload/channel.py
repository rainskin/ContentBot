from aiogram import types
from aiogram.dispatcher import FSMContext

import keyboards
import loader
from loader import dp, bot
from states import States


@dp.callback_query_handler(state=States.upload_channel)
async def upload(callback_query: types.CallbackQuery, state: FSMContext):
    chat_name = callback_query.data
    channel_name = ''
    chat_id = ''
    total_photos_count = loader.other_channels.count_documents({'channel': chat_name})

    if chat_name == 'anime_tyan':
        total_photos_count = loader.ecchi_col.count_documents({})
        await bot.send_message(callback_query.message.chat.id,
                               f'В базе {total_photos_count} постов. Контент для этого канала можешь загрузить через команду /parse')
        await state.finish()
        return

    elif chat_name == 'yuri':
        channel_name = 'Юри'

    elif chat_name == 'cute_pics':
        channel_name = 'Пикчи для диалогов'

    elif chat_name == 'avatars':
        channel_name = 'Крутые авы'

    elif chat_name == 'bubblekum':
        channel_name = 'Баблкам'

    elif chat_name == 'irl_characters':
        channel_name = 'Вымышленные персонажи'

    elif chat_name == 'zxc':
        channel_name = 'ZXC Авы'

    elif chat_name == 'hentai':
        total_photos_count = loader.hentai_coll.count_documents({})
        await bot.send_message(callback_query.message.chat.id,
                               f'В базе {total_photos_count} постов. Контент для этого канала можешь загрузить через команду /parse')
        await state.finish()
        return

    await bot.send_message(callback_query.message.chat.id,
                           f'Ты выбрал канал {channel_name}. В базе {total_photos_count} постов')
    await state.update_data(chat_name=chat_name, chat_id=chat_id)
    await bot.send_message(callback_query.message.chat.id,
                           'Отправляй сюда посты, которые хочешь добавить в базу, а потом нажми на кнопку',
                           reply_markup=keyboards.done_kb)
    await States.collect_pictures.set()
