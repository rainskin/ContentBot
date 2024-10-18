from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp
from states import States
from utils.check_admin_rights import is_admin




url = 'https://t.me/birzhayumor'

@dp.message_handler(commands='join')
async def cmd_join(msg: types.Message, state: FSMContext) -> None:
    if not is_admin(msg.from_user.id):
        return

    await msg.answer('Чтобы добавить юзербота в твои каналы, отправь любое сообщение')
    await state.set_state(States.waiting_chat_links)