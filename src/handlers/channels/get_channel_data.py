from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import BadRequest, Unauthorized

import keyboards
from core.db import channels
from loader import dp, bot, list_of_channels
from states import States


@dp.message_handler(state=States.get_channel_data, content_types='any')
async def get_channel_data(msg: types.Message, state: FSMContext):
    user_id = msg.from_user.id
    if msg.is_command():
        await msg.answer('Отправь команду еще раз')
        await state.finish()

    ## TODO: to figure out why the /start command does not work in this place

    if not msg.is_forward():
        await msg.answer(f'Нужен репост из канала. Отправь другое сообщение')
        return

    if not msg.forward_from_chat:
        await msg.answer(f'Это репост не из канала')
        return

    channel_username = msg.forward_from_chat.username
    channel_id = msg.forward_from_chat.id
    channel_title = msg.forward_from_chat.title

    try:
        await bot.get_chat_administrators(channel_id)
    except Unauthorized as e:
        await msg.answer('Нужно добавить бота в канал')
        return
    except BadRequest as e:
        if e.args == 'Member list is inaccessible':
            await msg.answer('Сначала сделай бота администратором')
            return
    except Exception as e:
        await msg.answer(f'Что-то пошло не так. {e.args}')
        return

    if not await channels.is_unique(channel_id):
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
