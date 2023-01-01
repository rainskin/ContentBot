# from envparse import env
from core.env import env


# env.read_envfile()


TOKEN = env.get('BOT_TOKEN')

login_page = "https://www.reddit.com/login/?dest=https%3A%2F%2Fwww.reddit.com%2Fr%2Fecchi%2F"
username = env.get('REDDIT_USERNAME')
password = env.get('REDDIT_PASSWORD')
url = "https://www.reddit.com/r/ecchi/new/"

API_ID = env.get_int('USERBOT_API_ID')
API_HASH = env.get('USERBOT_API_HASH')

UPLOAD_CHANNEL_LINK = env.get('UPLOAD_CHANNEL_LINK')
TEST_CHANNEL_ID = env.get_int('TEST_CHANNEL_ID')

ANIME_CHAN_ID = env.get_int('ANIME_CHAN_ID')
YURI_ID = env.get_int('YURI_ID')
CUTE_PICS_ID = env.get_int('CUTE_PICS_ID')
AVATARS_ID = env.get_int('AVATARS_ID')
BUBBLEKUM_ID = env.get_int('BUBBLEKUM_ID')
IRL_ID = env.get_int('IRL_ID')
ZXC_ID = env.get_int('ZXC_ID')
HENTAI_ID = env.get_int('HENTAI_ID')