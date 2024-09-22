from datetime import datetime

import config
import loader


class Users:

    def __init__(self):
        self.client = loader.ad_manager_db_client
        self.db = self.client[config.MONGO_DB_NAME]
        self.collection = self.db['users']

    async def add_user(self, name, username, user_id):

        doc = {
            'name': name,
            'username': username,
            'id': user_id,
            'registration_date': datetime.now(),
            'is_active': True,
        }

        await self.collection.insert_one(doc)

    async def is_new(self, user_id):
        doc = await self.collection.find_one({'id': user_id})
        return not bool(doc)
