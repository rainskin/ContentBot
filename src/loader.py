import motor.motor_asyncio
import pymongo
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import config
import userbot

db_client = pymongo.MongoClient(config.MONGO_URL)
db = db_client[config.MONGO_DB_NAME]
ad_manager_db_client = motor.motor_asyncio.AsyncIOMotorClient(config.MONGO_URL)
list_of_admins = db['list of admins']
list_of_channels = db['list of channels']
sales = db['sales']
msgs_to_delete = db['msgs_to_delete']

ecchi_col = db['reddit ecchi']
hentai_coll = db['Hentai']
blacklist = db['blacklist']
other_channels = db['other_channels']

bot = Bot(token=config.BOT_TOKEN, parse_mode='html')
dp = Dispatcher(bot, storage=MemoryStorage())
userbot = userbot.Userbot()
