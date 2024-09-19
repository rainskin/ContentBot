from aiogram import types

from loader import dp, userbot
from utils.check_admin_rights import is_superadmin


@dp.message_handler(commands='clear_cache', state='*')
async def cmd_test(msg: types.Message):
    if not is_superadmin(msg.from_user.id):
        return

    cache_store = userbot.app.message_cache.store
    cache_store.clear()
    await msg.answer(f'Очистил Pyrogram кэш сообщений. Текущий кэш\n\n{cache_store}')

