from src import loader


def is_new(url):
    if loader.ecchi_col.find_one({'url': url}) is None and loader.hentai_coll.find_one(
            {'url': url}) is None and loader.blacklist.find_one({'url': url}) is None:
        return True
    else:
        return False

