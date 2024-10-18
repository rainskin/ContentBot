from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import bot_command_scope

import keyboards
import texts
from config import UPLOAD_CHANNEL_ID
from core.db import users
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

ADMIN_COMMANDS = [
    types.BotCommand('start', 'Начать'),
    types.BotCommand('channels', 'Управление каналами'),
]

@dp.message_handler(commands='start', state='*')
async def cmd_start(msg: types.Message, state: FSMContext):
    await state.finish()
    chat_id = msg.chat.id
    chat_type = msg.chat.type
    user_id = msg.chat.id
    if chat_type == 'private':
        if is_superadmin(user_id):
            await msg.answer(texts.admin_commands, reply_markup=keyboards.remove)
            await dp.bot.set_my_commands(COMMANDS, scope=bot_command_scope.BotCommandScopeChat(chat_id=chat_id))

        elif is_admin(user_id):
            await msg.answer(texts.cmd_start_text, reply_markup=keyboards.remove)
            await dp.bot.set_my_commands(ADMIN_COMMANDS, scope=bot_command_scope.BotCommandScopeChat(chat_id=chat_id))
        else:
            await msg.answer('🤖 Бот находится в <b>режиме тестирования.</b>\n'
                             '🚫 Не блокируйте бота, чтобы получить <b>уведомление о публичном релизе</b>')

        await register_user(msg)

    elif chat_type == 'supergroup' or chat_type == 'chat':
        channel_owner_id = msg.from_user.id
        sale_group_id = await users.get_sale_group_id(channel_owner_id)

        if not sale_group_id:
            return

        is_service_group = chat_id == sale_group_id or chat_id == UPLOAD_CHANNEL_ID
        if not is_service_group:
            return

        await msg.answer("Бот перезапущен")




async def register_user(msg: types.Message):
    chat_id = msg.chat.id

    if not await users.is_new(chat_id):
        return

    name = msg.chat.full_name
    username = msg.chat.username
    await users.add_user(name, username, chat_id)
