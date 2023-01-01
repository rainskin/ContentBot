import pymongo
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import config
import userbot

db_client = pymongo.MongoClient(config.SERVER_IP, username='root',  password=config.MONGO_PASSWORD, authSource='admin')
images_db = db_client['images']

ecchi_col = images_db['reddit ecchi']
hentai_coll = images_db['Hentai']
blacklist = images_db['blacklist']
cute_pics = images_db['Cute_pics']
avatars = images_db['Avatars']
irl_pics = images_db['irl_pics']
zxc = images_db['ZXC']
yuri = images_db['yuri']
bubblecum = images_db['bubblecum']
other_channels = images_db['other_channels']

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
userbot = userbot.Userbot()
