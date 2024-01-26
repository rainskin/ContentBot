from aiogram import types
from aiogram.dispatcher import FSMContext

import keyboards
from loader import dp, bot, list_of_channels
from states import States


@dp.callback_query_handler(text='add_channel', state=States.channel_management)
async def _(query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    channels = data['channels']
    await bot.send_message(query.message.chat.id, 'Отправь мне сообщение с канала, который хочешь добавить')
    await bot.delete_message(query.message.chat.id, channels)
    await query.answer()
    await States.get_channel_data.set()


@dp.message_handler(state=States.get_channel_data, content_types=types.ContentType.ANY)
async def get_channel_data(msg: types.Message, state: FSMContext):

    if not msg.is_forward():
        await msg.answer(f'Нужен репост из канала. Отправь другое сообщение')
        return

    if msg.forward_from_chat:

        channel_username = msg.forward_from_chat.username
        channel_id = msg.forward_from_chat.id
        channel_title = msg.forward_from_chat.title

        if not is_unique(channel_id):
            await msg.answer(f'Канал {channel_title} уже добавлен в базу')
            return

        await state.update_data(channel_id=channel_id, channel_title=channel_title)

        if channel_username:
            link = 'https://t.me/' + channel_username

            await msg.answer(f'Добавляем канал <b>{channel_title}</b>?\n<b>Ссылка:</b> {link}\n<b>ID</b>: {channel_id}',
                             reply_markup=keyboards.YesOrNo(), parse_mode='html', disable_web_page_preview=True)
            await state.update_data(link=link)
            await States.add_channel.set()

        else:
            await msg.answer('Теперь отправь ссылку на канал')
            await States.get_channel_link.set()

    else:
        await msg.answer(f'Это репост не из канала')


def is_unique(channel_id):
    return not list_of_channels.find_one({'id': channel_id})
