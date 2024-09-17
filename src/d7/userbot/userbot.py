from .client import Client


class Userbot:
    def __init__(self, session_string: str):
        self.client = Client("userbot", session_string=session_string)

    async def get_session_string(self):  # TODO
        return await self.client.export_session_string()
