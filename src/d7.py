from aiogram import Bot, Dispatcher
from d7 import run_app, env, register_handlers
from d7 import db

BOT_TOKEN = env.parse_str("BOT_TOKEN")
bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot)

register_handlers(dp)

MONGO_URL = env.parse_str("MONGO_URL")
MONGO_DB = env.parse_str("MONGO_DB")


async def test():
    await db.channels.create(1, "Channel1", "https://t.me/channel1")
    print(await db.channels.get_ids())


async def on_startup():
    db.connect(MONGO_URL, MONGO_DB)
    await test()
    print("App started.")


run_app(dp, on_startup)
