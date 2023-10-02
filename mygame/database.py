from pymongo import MongoClient
from random import randint
from mygame.config_parser import get_db_host, get_db_port, get_start_credit


class MongoDB:
    def __init__(self):
        self.client = MongoClient(get_db_host(), get_db_port())
        self.db = self.client["game-database"]

    def update_user(self, data):
        collection = self.db.user
        collection.update_one({
            'id': data['id'],
            'name': data['name']
        },
            {'$set': {
                'items': data['items'],
                'credit': data['credit'],
            }})

    def find_user(self, user_name: str) -> dict:
        collection = self.db.user
        user: dict = collection.find_one({'name': user_name})
        if not user:
            return {'user_name': user_name}
        user.pop('_id', None)
        return user

    def create_user(self, user_name: str) -> dict:
        collection = self.db.user

        user = {
            'name': user_name,
            'id': randint(1000000, 10000000),
            'credit': get_start_credit(),
            'items': []
        }

        try:
            collection.insert_one(user)
        except Exception as e:
            raise e
        else:
            del user['_id']
            return user

    def find_items(self) -> list[dict]:
        collection = self.db.item
        items = collection.find()
        items_list = []
        for item in items:
            item.pop('_id', None)
            items_list.append(item)
        return items_list
