from aiogram import types
from aiogram.dispatcher import FSMContext

import keyboards
import loader
from loader import dp, bot, list_of_channels
from states import States


@dp.callback_query_handler(state=States.upload_channel)
async def upload(query: types.CallbackQuery, state: FSMContext):
    channel_id = int(query.data)
    channel = list_of_channels.find_one({'id': channel_id})
    channel_name = str(channel['title'])

    total_photos_count = loader.other_channels.count_documents({'channel_id': channel_id})

    if 'anime tyans' in channel_name.lower():
        total_photos_count = loader.ecchi_col.count_documents({})
        await bot.send_message(query.message.chat.id,
                               f'В базе {total_photos_count} постов. Контент для этого канала можешь загрузить через команду /parse')

        await query.answer()
        await state.finish()
        return

    if 'vip tyan' in channel_name.lower():
        total_photos_count = loader.hentai_coll.count_documents({})
        await bot.send_message(query.message.chat.id,
                               f'В базе {total_photos_count} постов. Контент для этого канала можешь загрузить через команду /parse')
        await query.answer()
        await state.finish()
        return

    await bot.send_message(query.message.chat.id,
                           f'Ты выбрал канал <b>{channel_name}</b>. В базе {total_photos_count} постов', parse_mode='html')
    await state.update_data(channel_name=channel_name, channel_id=channel_id)
    await bot.send_message(query.message.chat.id,
                           'Отправляй сюда посты, которые хочешь добавить в базу, а потом нажми на кнопку',
                           reply_markup=keyboards.done_kb)
    await States.collect_pictures.set()
