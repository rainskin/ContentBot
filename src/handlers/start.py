from aiogram import types
from aiogram.dispatcher import FSMContext

import texts
from loader import dp

COMMANDS = [
    types.BotCommand('start', 'Начать'),
    types.BotCommand('auth', 'Авторизация'),
    types.BotCommand('parse', 'Начать парсинг'),
    types.BotCommand('show', 'Посмотреть фотки'),
    types.BotCommand('test', 'Тестиров_Очка'),
    types.BotCommand('upload', 'Загрузить контент'),
    types.BotCommand('schedule', 'Запланировать посты')
]


@dp.message_handler(commands='start', state='*')
async def cmd_start(message: types.Message, state: FSMContext):
    # if message.from_user.id not in config.ADMIN_ID:
    #     return
    await state.finish()
    await message.answer(texts.cmd_start_text)
    await dp.bot.set_my_commands(COMMANDS)
