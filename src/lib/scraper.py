import httpx

BASE_URL = 'https://gateway.reddit.com/desktopapi/v1/subreddits/ecchi'

# noinspection SpellCheckingInspection
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
}

PARAMS = {
    'rtj': 'only',
    'allow_over18': 1,
    'sort': 'new',
}


async def get_pictures() -> list[str]:
    client = httpx.AsyncClient(params=PARAMS, headers=HEADERS)

    async with client:
        resp = await client.get(BASE_URL)

    result = resp.json()
    posts = result['posts'].values()
    return _parse_pictures(posts)


def _parse_pictures(posts: list[dict]) -> list[str]:
    pictures = set()

    for post in posts:
        media = post['media']

        if 'content' in media:
            if media['type'] == 'image':
                picture = media['resolutions'][-1]['url']
                pictures.add(picture)

    return list(pictures)
