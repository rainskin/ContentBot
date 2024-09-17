from dataclasses import asdict, dataclass
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection


@dataclass
class PostDocument:
    template_id: str
    publish_date: int
    delete_date: int
    published: bool = False
    id: str = None


# TODO: refactor
class PostsCollection:
    def __init__(self, raw: AsyncIOMotorCollection):
        self._raw = raw

    async def create(
        self,
        template_id: str,
        publish_date: int,
        delete_date: int,
    ):
        doc = PostDocument(template_id, publish_date, delete_date)
        result = await self._raw.insert_one(asdict(doc))
        doc.id = str(result.inserted_id)
        return doc

    async def save(self, doc: PostDocument):
        filter = {"_id": ObjectId(id)}
        data = asdict(doc)
        del data["id"]
        await self._raw.replace_one(filter, data)

    async def get(self, id: str):  # TODO: refactor
        filter = {"_id": ObjectId(id)}
        data = await self._raw.find_one(filter)
        data["id"] = str(data["_id"])
        return PostDocument(**data)

    async def get_all(self):
        cursor = self._raw.find()
        docs: list[PostDocument] = []
        async for data in cursor:
            data["id"] = str(data["_id"])
            doc = PostDocument(**data)
            docs.append(doc)
        return docs
