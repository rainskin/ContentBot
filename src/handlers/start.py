from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import bot_command_scope

import keyboards
import texts
from config import SALE_GROUP_ID
from loader import dp
from utils.check_admin_rights import is_admin, is_superadmin

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

    if msg.chat.id != SALE_GROUP_ID and is_superadmin(msg.chat.id):
        await msg.answer(texts.admin_commands, reply_markup=keyboards.remove)
    else:
        await msg.answer("Бот перезапущен")
    await state.finish()
    await dp.bot.set_my_commands(COMMANDS, scope=bot_command_scope.BotCommandScopeChat(chat_id=936845322))
