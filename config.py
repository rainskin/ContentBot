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
TYAN_ID = -1001191474106

TEST_CHANNEL_ID = -1001862978453
YURI_ID=-1001611457973
CUTE_PICS_ID = -1001554954940
AVATARS_ID = -1001592432164
