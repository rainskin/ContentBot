from aiogram import types
from aiogram.dispatcher import FSMContext

import keyboards
from loader import dp, list_of_admins, bot
from states import States
from utils.check_admin_rights import is_admin



@dp.message_handler(state=States.get_channel_link)
async def _(msg: types.Message, state: FSMContext):

    if not msg.entities:
        await msg.answer('Просто отправь ссылку на канал')
        return

    if msg.entities[0].type != 'url':
        await msg.answer('Нужна только ссылка')
        return

    data = await state.get_data()

    entity = msg.entities[0]
    offset = entity.offset
    length = entity.length

    link = msg.text[offset:offset + length]
    channel_id = data['channel_id']
    channel_title = data['channel_title']

    await msg.answer(f'Добавляем канал <b>{channel_title}</b>?\n<b>Ссылка:</b> {link}\n<b>ID</b>: {channel_id}', reply_markup=keyboards.YesOrNo(),parse_mode='html', disable_web_page_preview=True)
    await state.update_data(link=link)
    await States.add_channel.set()

