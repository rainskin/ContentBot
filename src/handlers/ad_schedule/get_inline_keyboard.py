from aiogram import types
from aiogram.dispatcher import FSMContext

import keyboards
from config import SALE_GROUP_ID
from handlers.ad_schedule.schedule_ad import delete_messages
from loader import dp, userbot, bot
from states import States
from utils import db
from utils.check_admin_rights import is_salesman, is_admin


@dp.message_handler(state=States.take_inline_keyboard)
async def _(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    service_msg_ids = data.get('service_msg_ids', [])
    last_preview_msg_id = data.get('last_preview_msg_id')
    await state.update_data(service_msg_ids=service_msg_ids + [msg.message_id])

    if last_preview_msg_id:
        try:
            await bot.delete_message(msg.chat.id, last_preview_msg_id)
        except Exception as e:
            pass
        await state.update_data(last_preview_msg_id=None)

    try:
        keyboard_data = msg.text
        text = (f'Вот так будет выглядеть клавиатура\n\n'
                f'Если хочешь заменить, просто отправь новую в следующем сообщении')
        try:
            answer = await msg.answer(text,
                                  reply_markup=keyboards.InlineKeyboardBuilder(keyboard_data, is_preview=True))
        except ValueError as e:
            await msg.answer(str(e))
            return
        await state.update_data(keyboard_data=keyboard_data, last_preview_msg_id=answer.message_id)

    except Exception as e:
        error_answer = await msg.answer('Что-то пошло не так. Отправь кнопки в следующем формате:')
        await state.update_data(last_preview_msg_id=error_answer.message_id)


@dp.callback_query_handler(state=States.take_inline_keyboard, text='accept_inline_keyboard')
async def _(query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    service_msg_ids = data.get('service_msg_ids', [])
    await delete_messages(query.message.chat.id, service_msg_ids)
    await state.update_data(service_msg_ids=[])
    await state.set_state(States.schedule_ad)
    await query.message.delete()
