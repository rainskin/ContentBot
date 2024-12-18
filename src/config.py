from core.env import env

BOT_TOKEN = env.get('BOT_TOKEN')


MONGO_URL = env.get('MONGO_URL')
MONGO_DB_NAME = env.get('MONGO_DB_NAME')

login_page = "https://www.reddit.com/login/?dest=https%3A%2F%2Fwww.reddit.com%2Fr%2Fecchi%2F"
url = "https://www.reddit.com/r/ecchi/new/"

API_ID = env.get_int('API_ID')
API_HASH = env.get('API_HASH')

UPLOAD_CHANNEL_LINK = env.get('UPLOAD_CHANNEL_LINK')
UPLOAD_CHANNEL_ID = env.get_int('UPLOAD_CHANNEL_ID')
SALE_GROUP_ID = env.get_int('SALE_GROUP_ID')

USERBOT_ID = env.get_int('USERBOT_ID')
USERBOT_SESSION_STRING = env.get('USERBOT_SESSION_STRING')
