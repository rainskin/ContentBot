from motor.motor_asyncio import AsyncIOMotorCollection


class ChannelsCollection:
    def __init__(self, raw: AsyncIOMotorCollection):
        self._raw = raw

    async def create(self, id: int, title: str, link: str):
        doc = {"title": title, "link": link, "id": id}
        await self._raw.insert_one(doc)

    async def get_ids(self) -> list[int]:  # TODO
        return await self._raw.distinct("id")
