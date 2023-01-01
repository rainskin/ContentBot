from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import bot_command_scope

import texts
from loader import dp

COMMANDS = [
    types.BotCommand('start', 'Начать'),
    types.BotCommand('parse', 'Начать парсинг'),
    types.BotCommand('show', 'Посмотреть фотки'),
    types.BotCommand('test', 'Тестиров_Очка'),
    types.BotCommand('upload', 'Загрузить контент'),
    types.BotCommand('schedule', 'Запланировать посты')
]


@dp.message_handler(commands='start', state='*')
async def cmd_start(msg: types.Message, state: FSMContext):
    if msg.from_user.id != 936845322:
        await msg.answer('Нет доступа')
    else:
        await state.finish()
        await msg.answer(texts.cmd_start_text)
        await dp.bot.set_my_commands(COMMANDS, scope=bot_command_scope.BotCommandScopeChat(chat_id=936845322))
