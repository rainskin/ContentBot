import config
import loader


class Channels:

    def __init__(self):
        self.client = loader.ad_manager_db_client
        self.db = self.client[config.MONGO_DB_NAME]
        self.user_collection = self.db['users']
        self.channel_collection = self.db['channels']

    async def add_channel(self, user_id: int, channel_info: dict):
        await self.user_collection.update_one({'id': user_id}, {'$push': {'channels': channel_info}}, upsert=True)

        channel_info['owner_id'] = user_id
        await self.channel_collection.insert_one(channel_info)

    async def get_channels(self, user_id: int) -> list[dict]:
        doc = await self.user_collection.find_one({'id': user_id})
        return doc.get('channels', [])

    async def remove_channel(self, user_id: int, channel_id: int):
        await self.user_collection.update_one({'id': user_id}, {'$pull': {'channels': {'id': channel_id}}})
        await self.channel_collection.delete_one({'id': user_id})

    # async def get_channel_by_id(self, channel_id: int) -> dict | None:
    #     doc = await self.channel_collection.find_one({'id': channel_id})
    #     print('doc', doc)
    #     channels = doc.get('channels')
    #     for channel in channels:
    #         if channel['id'] == channel_id:
    #             return channel
    #     return None

    async def get_channel_by_id(self, channel_id: int) -> dict | None:
        return await self.channel_collection.find_one({'id': channel_id})

    async def get_owner_id_by_channel_id(self, channel_id: int):
        doc = await self.channel_collection.find_one({'id': channel_id})

        return doc.get('owner_id') if doc else None

    async def is_unique(self, channel_id: int):
        return not bool(await self.channel_collection.find_one({'id': channel_id}))

    async def get_channels_titles_by_id(self, user_id: int, channel_ids: list[int]):
        doc = await self.user_collection.find_one({'id': user_id})
        channels = doc.get('channels')
        titles = []

        for channel_id in channel_ids:
            for channel in channels:
                if channel['id'] == channel_id:
                    titles.append(channel['title'])

        return titles

    async def get_channel_links_by_id(self, user_id: int, channel_ids: list[int]):
        doc = await self.user_collection.find_one({'id': user_id})
        channels = doc.get('channels')
        links = []

        for channel_id in channel_ids:
            for channel in channels:
                if channel['id'] == channel_id:
                    links.append(channel['link'])

        return links

    async def get_channel_link_by_title(self, user_id: int, title: str):
        doc = await self.user_collection.find_one({'id': user_id})
        channels = doc.get('channels')

        for channel in channels:
            if channel['title'] == title:
                return channel['link']

        return None

    async def is_exists(self, channel_id: int):
        return bool(await self.channel_collection.find_one({'id': channel_id}))

    async def set_userbot_status(self, channel_id: int, status: bool):
        await self.channel_collection.update_one({'id': channel_id}, {'$set': {'userbot_status': status}}, upsert=True)

    async def get_userbot_status(self, channel_id: int):
        doc = await self.channel_collection.find_one({'id': channel_id})
        return doc.get('userbot_status')