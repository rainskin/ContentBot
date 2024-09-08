import httpx

BASE_URL = 'https://gateway.reddit.com/desktopapi/v1/subreddits/ecchi'

# noinspection SpellCheckingInspection
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/113.0',
}

PARAMS = {
    'rtj': 'only',
    'allow_over18': 1,
    'sort': 'new',
}


async def get_pictures() -> list[str]:
    client = httpx.AsyncClient(params=PARAMS, headers=HEADERS)
    print('Getting', client)
    async with client:
        resp = await client.get(BASE_URL)
        print(f'Делаю запрос, запрос = {resp}')

    result = resp.json()
    posts = result['posts'].values()
    print(f'посты = {posts}')
    return _parse_pictures(posts)


def _parse_pictures(posts: list[dict]) -> list[str]:
    pictures = set()

    for post in posts:
        media = post['media']

        if media and 'content' in media:
            if media['type'] == 'image':
                picture = media['resolutions'][-1]['url']
                pictures.add(picture)

    return list(pictures)
