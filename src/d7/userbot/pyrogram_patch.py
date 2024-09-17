import pyrogram.utils


def get_peer_type(peer_id: int) -> str:
    if peer_id > 0:
        return "user"
    if str(peer_id).startswith("-100"):
        return "channel"
    return "chat"


def patch_pyrogram():
    pyrogram.utils.get_peer_type = get_peer_type
