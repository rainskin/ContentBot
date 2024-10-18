from aiogram import types
from aiogram.dispatcher import FSMContext

import keyboards
from loader import dp, userbot, bot
from states import States


async def request_inline_keyboard(query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    is_album = data.get('is_album')
    drop_author = data.get('drop_author')
    if is_album or drop_author:
        await query.answer('Для альбомов и репостов клавиатура не поддерживается')
        return

    answer = await query.message.answer('Отправь клавиатуру', reply_markup=keyboards.AddOneButton(keyboards.cancel_current_action))

    await state.update_data(service_msg_ids=[answer.message_id])
    await query.answer()
    await state.set_state(States.take_inline_keyboard)


async def remove_inline_keyboard(query: types.CallbackQuery, state):
    await state.update_data(keyboard_data=None)
    await toggle_parameter(query.message.chat.id, state, inline_keyboard=True)
    await query.answer('Клавиатура удалена', show_alert=True)


async def request_autodelete_timer(query, state):

    text = f'Через какое время удалить пост? Нажми кнопку или укажи время вручную в формате <i>hh:mm</i>'
    answer = await query.message.answer(text, reply_markup=keyboards.AutodeleteTimerAmount())

    await state.update_data(msg_with_autodelete_timer=answer.message_id)
    await query.answer()
    await state.set_state(States.take_autodelete_timer)


@dp.callback_query_handler(state=States.schedule_ad)
async def customize_post(query: types.CallbackQuery, state: FSMContext):
    text = query.data
    data = await state.get_data()
    inline_keyboard_value = data.get('inline_keyboard')
    if text == 'add_inline_keyboard':
        await request_inline_keyboard(query, state)
        return
    if text == 'remove_inline_keyboard':
        await remove_inline_keyboard(query, state)
        return
    if text == 'set_autodelete_timer':
        await request_autodelete_timer(query, state)
        return
    if text == 'toggle_notification':
        await toggle_parameter(query.message.chat.id, state, notification=True)
    elif text == 'toggle_author':
        if inline_keyboard_value:
            await remove_inline_keyboard(query, state)
        await toggle_parameter(query.message.chat.id, state, drop_author=True)

async def toggle_parameter(chat_id, state, drop_author=False, notification=False, inline_keyboard=False, autodelete_timer=False):
    data = await state.get_data()
    ad_title_msg_id = data.get('ad_title_msg_id')
    drop_author_value = data['drop_author']
    notification_value = data['notification']
    inline_keyboard_value = data.get('inline_keyboard')
    autodelete_timer_value = data.get('autodelete_timer')

    is_changed = False

    if drop_author:
        drop_author_value = not drop_author_value
        is_changed = True
    if notification:
        notification_value = not notification_value
        is_changed = True
    if inline_keyboard:
        inline_keyboard_value = not inline_keyboard_value
        is_changed = True
    if autodelete_timer:
        is_changed = True

    if is_changed:
        await state.update_data(drop_author=drop_author_value, notification=notification_value, inline_keyboard=inline_keyboard_value)
        await bot.edit_message_reply_markup(chat_id, ad_title_msg_id, reply_markup=keyboards.AdPostSettings(drop_author=drop_author_value, notification=notification_value,
                                                                       inline_keyboard=inline_keyboard_value, auto_delete_timer=autodelete_timer_value))
        # await query.message.edit_reply_markup(keyboards.AdPostSettings(drop_author=drop_author_value, notification=notification_value,
        #                                                                inline_keyboard=inline_keyboard_value, auto_delete_timer=autodelete_timer_value))
        # await query.answer()
