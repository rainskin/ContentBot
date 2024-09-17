from motor.motor_asyncio import AsyncIOMotorClient
from .collections import ChannelsCollection, PostTemplatesCollection, PostsCollection


class Database:
    def __init__(self):
        self.channels: ChannelsCollection = None
        self.post_templates: PostTemplatesCollection = None
        self.posts: PostsCollection = None

    def connect(self, mongo_url: str, database_name: str):
        client = AsyncIOMotorClient(mongo_url, database_name)
        db = client[database_name]
        self.channels = ChannelsCollection(db["list of channels"])
        self.post_templates = PostTemplatesCollection(db["d7_post_templates"])
        self.posts = PostsCollection(db["d7_posts"])


db = Database()
