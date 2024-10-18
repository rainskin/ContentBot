from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.ad_schedule.post_setting_callback_handlers import toggle_parameter
from loader import dp, bot
from states import States
from utils.callback_templates import autodelete_timer_is_template
from utils.timedelta_parser import parse_hours_and_minutes


@dp.message_handler(state=States.take_autodelete_timer)
async def _(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    msg_with_autodelete_timer = data.get('msg_with_autodelete_timer')

    try:
        hour, minutes = parse_hours_and_minutes(msg.text)
    except ValueError as e:
        await msg.answer(str(e))
        return

    text = f'Пост будет удален через {hour} час(ов) {minutes} минут'
    answer = await msg.answer(text)

    service_msg_ids = data.get('service_msg_ids', [])
    current_autodelete_timer = data.get('autodelete_timer')
    new_autodelete_timer = f'{hour}:{minutes}'

    await state.update_data(service_msg_ids=service_msg_ids + [msg.message_id, answer.message_id], autodelete_timer=new_autodelete_timer)
    await bot.delete_message(msg.chat.id, msg_with_autodelete_timer)

    if new_autodelete_timer != current_autodelete_timer:
        await toggle_parameter(msg.chat.id, state, autodelete_timer=True)
    await state.set_state(States.schedule_ad)


@dp.callback_query_handler(state=States.take_autodelete_timer)
async def _(query: types.CallbackQuery, state: FSMContext):

    inline_keyboard_data = query.data
    data = await state.get_data()
    current_autodelete_timer = data.get('autodelete_timer')
    if inline_keyboard_data.startswith(autodelete_timer_is_template()):
        new_autodelete_timer = inline_keyboard_data.replace(autodelete_timer_is_template(), '')
        await state.update_data(autodelete_timer=new_autodelete_timer)
    else:
        new_autodelete_timer = None
        await state.update_data(autodelete_timer=new_autodelete_timer)

    if new_autodelete_timer != current_autodelete_timer:
        await toggle_parameter(query.message.chat.id, state, autodelete_timer=True)
    await state.set_state(States.schedule_ad)
    await query.message.delete()
