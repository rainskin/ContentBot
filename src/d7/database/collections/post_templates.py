from dataclasses import asdict, dataclass
from typing import Literal
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection

PostType = Literal["photo", "video", "text"]


@dataclass
class PostButton:
    text: str
    url: str


PostButtons = list[list[PostButton]]


@dataclass
class PostTemplateDocument:
    text: str
    type: PostType
    files: list[str]
    buttons: PostButtons
    id: str = None


class PostTemplatesCollection:
    def __init__(self, raw: AsyncIOMotorCollection):
        self._raw = raw

    async def create(
        self,
        text: str,
        type: PostType,
        files: list[str] = None,
        buttons: PostButtons = None,
    ):
        doc = PostTemplateDocument(text, type, files or [], buttons or [])
        result = await self._raw.insert_one(asdict(doc))
        doc.id = str(result.inserted_id)
        return doc

    async def get(self, id: str):
        data = await self._raw.find_one({"_id": ObjectId(id)})
        data["id"] = str(data["_id"])
        return PostTemplateDocument(**data)
