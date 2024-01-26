from core.env import env

BOT_TOKEN = env.get('BOT_TOKEN')


MONGO_URL = env.get('MONGO_URL')
MONGO_DB_NAME = env.get('MONGO_DB_NAME')

# SERVER_IP = env.get('SERVER_IP')
# MONGO_PASSWORD = env.get('MONGO_PASSWORD')

login_page = "https://www.reddit.com/login/?dest=https%3A%2F%2Fwww.reddit.com%2Fr%2Fecchi%2F"
# username = env.get('REDDIT_USERNAME')
# password = env.get('REDDIT_PASSWORD')
url = "https://www.reddit.com/r/ecchi/new/"

API_ID = env.get_int('API_ID')
API_HASH = env.get('API_HASH')

UPLOAD_CHANNEL_LINK = env.get('UPLOAD_CHANNEL_LINK')
UPLOAD_CHANNEL_ID = env.get_int('UPLOAD_CHANNEL_ID')

USERBOT_SESSION_STRING = env.get('USERBOT_SESSION_STRING')
CH_SESSION_STRING = env.get('CH_SESSION_STRING')
