from random import randint
from mygame.database import MongoDB


def filling_db():
    mongo = MongoDB()
    mongo.set_collection('Items')
    coll = mongo.collection
    items = items_generators()
    coll.insert_many(items)


def items_generators() -> list[dict]:
    list_items = []
    for index in range(100):
        num = randint(1, 5)
        list_items.append({
            'id': randint(1000000, 10000000),
            'name': get_item_type(num) + f' # {index}',
            'price': generation_price(num),
            'description': 'Some description'
         })

    return list_items


def get_item_type(num: int) -> str:
    switch = {
        1: 'Weapon',
        2: 'Armor',
        3: 'Vehicle',
        4: 'Aircraft',
        5: 'Consumables'
    }
    return switch.get(num)


def generation_price(num: int) -> int:
    switch = {
        1: randint(1000, 5000),
        2: randint(1000, 5000),
        3: randint(5_000, 25_000),
        4: randint(50_000, 250_000),
        5: randint(100, 500)
    }
    return switch.get(num)


if __name__ == "__main__":
    filling_db()
