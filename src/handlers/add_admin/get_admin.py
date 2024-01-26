from aiogram import types
from aiogram.dispatcher import FSMContext

import keyboards
from loader import dp, bot
from states import States
from utils.check_admin_rights import is_admin


@dp.message_handler(state=States.waiting_msg_from_user)
async def _(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    previews_ids = data['previews_ids']
    if previews_ids:
        await delete_previews(msg.chat.id, previews_ids, state)

    if not msg.is_forward():
        await msg.answer(f'Нужен репост. Отправь другое сообщение')
        return

    try:
        name = msg.forward_from.first_name
        tg_id = msg.forward_from.id
    except AttributeError as e:
        await msg.answer('Аккаунт пользователя скрыт. Не могу добавить')
        return

    if not is_admin(tg_id):
        kb = keyboards.YesOrNo()
        await state.update_data(name=name, tg_id=tg_id)
        preview = await msg.answer(f'Добавить админа\n\n <b>{name}</b>\n id: <code>{tg_id}</code> ?', 'html', reply_markup=kb)
        await state.update_data(preview=preview.message_id)
        await States.add_admin.set()
    else:
        await msg.answer(f'{name} уже является админом')


async def delete_previews(chat_id: int, msg_ids: list, state: FSMContext):
    for msg_id in msg_ids:
        await bot.delete_message(chat_id, msg_id)
    await state.update_data(previews_ids=None)

