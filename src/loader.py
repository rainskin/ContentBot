import motor.motor_asyncio
import pymongo
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import config
import userbot

db_client = pymongo.MongoClient(config.MONGO_URL)
images_db = db_client[config.MONGO_DB_NAME]
ad_manager_db_client = motor.motor_asyncio.AsyncIOMotorClient(config.MONGO_URL)
list_of_admins = images_db['list of admins']
list_of_channels = images_db['list of channels']
sales = images_db['sales']
msgs_to_delete = images_db['msgs_to_delete']

ecchi_col = images_db['reddit ecchi']
hentai_coll = images_db['Hentai']
blacklist = images_db['blacklist']
other_channels = images_db['other_channels']

bot = Bot(token=config.BOT_TOKEN, parse_mode='html')
dp = Dispatcher(bot, storage=MemoryStorage())
userbot = userbot.Userbot()
