from envparse import env

env.read_envfile()

path = "C:\\Users\\TRVL\\PycharmProjects\\TrainingBot\\src\\chromedriver\\chromedriver.exe"

TOKEN = env('TOKEN')

login_page = "https://www.reddit.com/login/?dest=https%3A%2F%2Fwww.reddit.com%2Fr%2Fecchi%2F"
username = env('USERNAME')
password = env('PASSWORD')
url = "https://www.reddit.com/r/ecchi/new/"

API_ID = env('API_ID')
API_HASH = env('API_HASH')
TYAN_ID = env('TYAN_ID')

TEST_CHANNEL_ID = env('TEST_CHANNEL_ID')
YURI_ID = env('YURI_ID')
CUTE_PICS_ID = env('CUTE_PICS_ID')
AVATARS_ID = env('AVATARS_ID')
