from aiogram import types
from aiogram.dispatcher import FSMContext

import config
import keyboards
import loader
from loader import dp, bot
from states import States
from userbot import userbot


@dp.message_handler(state=States.collect_pictures, content_types=['photo'])
async def _(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    message_ids = data.get('message_ids', [])

    if msg.media_group_id is not None:
        # data = await state.get_data()
        group_id_in_data = data.get('group_id')

        if group_id_in_data == msg.media_group_id:
            pass

        else:
            group_id = msg.media_group_id

            await state.update_data(group_id=group_id)
            new_message_id = msg.message_id
            await state.update_data(message_ids=message_ids + [new_message_id])
            # print(msg_id)
            # await userbot.copy_media_group(chat_id=config.TEST_CHANNEL_ID, msg=new_message_id)

    else:

        new_message_id = msg.message_id
        # data = await state.get_data()
        message_ids = data.get('message_ids', [])
        await state.update_data(message_ids=message_ids + [new_message_id])


@dp.message_handler(state=States.collect_pictures)
async def _(msg: types.Message, state: FSMContext):
    data = await state.get_data()

    if msg.text == 'Готово':
        if 'message_ids' in data:
            photos = data['message_ids']
            chat_name = data['chat_name']
            number_of_photos = len(photos)
            await bot.send_message(msg.chat.id, f'Получено постов: {number_of_photos}\nНачинаю загрузку',
                                   reply_markup=keyboards.remove)

            for photo in photos:
                item = {
                    'msg_id': photo,
                    'channel': chat_name
                }
                loader.other_channels.insert_one(item)

            await bot.send_message(msg.chat.id, 'Загружено в базу данных')
            await state.finish()

        else:
            await bot.send_message(msg.chat.id, 'Сначала отправь фото для загрузки')

    else:
        await bot.send_message(msg.chat.id, 'Отправляй пикчи прямо сюда')
