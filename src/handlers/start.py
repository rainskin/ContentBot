from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import bot_command_scope

import keyboards
import texts
from loader import dp
from utils.check_admin_rights import is_admin

COMMANDS = [
    types.BotCommand('start', 'Начать'),
    types.BotCommand('parse', 'Начать парсинг'),
    types.BotCommand('show', 'Посмотреть фотки'),
    types.BotCommand('test', 'Тестиров_Очка'),
    types.BotCommand('upload', 'Загрузить контент'),
    types.BotCommand('schedule', 'Запланировать посты'),
    types.BotCommand('add_admin', 'Добавить нового админа')
]


@dp.message_handler(commands='start', state='*')
async def cmd_start(msg: types.Message, state: FSMContext):
    if not is_admin(msg.from_user.id):
        await msg.answer('Нет доступа')
    else:
        await state.finish()
        await msg.answer(texts.cmd_start_text, reply_markup=keyboards.remove)
        await dp.bot.set_my_commands(COMMANDS, scope=bot_command_scope.BotCommandScopeChat(chat_id=936845322))
