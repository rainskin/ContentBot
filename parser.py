import pyrogram
from pyrogram import filters

import config

app = pyrogram.Client('../userbot', config.API_ID, config.API_HASH)

@app.on_message(filters.chat())
def add_picture(_, msg: types.Message):