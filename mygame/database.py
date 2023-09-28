from pymongo import MongoClient
from random import randint
from mygame.config_parser import get_db_host, get_db_port, get_start_credit
from mygame.schemas import User, Item


class MongoDB:
    def __init__(self):
        self.client = MongoClient(get_db_host(), get_db_port())
        self.db = self.client["game-database"]
        self.collection = self.db.user

    def set_collection(self, coll_name) -> None:
        if coll_name == 'Users':
            self.set_user_collection()
        if coll_name == 'Items':
            self.set_item_collection()

    def set_user_collection(self) -> None:
        self.collection = self.db.user

    def set_item_collection(self) -> None:
        self.collection = self.db.item

    def update_user(self, data):
        self.set_user_collection()
        self.collection.update_one({
            'id': data['id'],
            'name': data['name']
        },
            {'$set': {
                'items': data['items'],
                'credit': data['credit'],
            }})

    def find_user(self, user_name: str) -> User:
        self.set_user_collection()
        search_result: dict = self.collection.find_one({'name': user_name})
        if not search_result:
            return User({'user_name': user_name})
        return User(search_result)

    def create_user(self, user_name: str) -> User:
        self.set_user_collection()
        user = {
            'name': user_name,
            'id': randint(1000000, 10000000),
            'credit': get_start_credit(),
            'items': []
        }

        try:
            self.db_insert(user, 'Users')
        except Exception as e:
            raise e
        else:
            return User(user)

    def find_items(self) -> list[dict]:
        self.set_item_collection()
        search_result = self.collection.find()
        items_list = [Item(obj).to_dict() for obj in list(search_result)]

        return items_list

    def db_insert(self, data2db: dict, name_coll) -> None:
        self.set_collection(name_coll)
        self.collection.insert_one(data2db)

