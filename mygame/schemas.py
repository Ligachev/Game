class Item:

    def __init__(self, obj: dict):
        self.id = obj['id']
        self.price = obj['price']
        self.name = obj['name']
        self.description = obj['description']

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'price': self.price,
            'name': self.name,
            'description': self.description,
        }


class User:

    def __init__(self, user_params: dict):
        self.is_login = True
        self.name = user_params.get('name')
        self.id = user_params.get('id')
        self.credit = user_params.get('credit')
        self.items = [Item(item) for item in user_params.get('items', [])]

    def create_user(self, user_params: dict):
        self.name = user_params.get('name')
        self.id = user_params.get('id')
        self.credit = user_params.get('credit')
        self.items = [item.to_item() for item in user_params.get('items', [])]

    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'id': self.id,
            'credit': self.credit,
            'items': [item.to_dict() for item in self.items]
        }

    def credits_update(self, new_credit: int) -> None:
        self.credit = new_credit

    def update_items(self, items: list[Item]) -> None:
        self.items = items

    def credits(self) -> int:
        return self.credit

    def get_items(self) -> list[dict]:
        return [item.to_dict() for item in self.items]


class ClientStorage:

    def __init__(self, is_login: bool, is_active: bool, page: str):
        self.user: User
        self.is_login: bool = is_login
        self.is_active: bool = is_active
        self.page: str = page
        self.items: list[Item] = []
        self.is_purchases: bool = False
        self.sys_message: str = ''

    def __getitem__(self, item):
        match item:
            case 'user':
                return self.user
            case 'is_login':
                return self.is_login
            case 'is_active':
                return self.is_active
            case 'page':
                return self.page
            case 'items':
                return self.items
            case 'is_purchases':
                return self.is_purchases
            case 'sys_message':
                return self.sys_message

    def print_store(self):
        print({
            'user': self.user.to_dict(),
            'is_login': self.is_login,
            'is_active': self.is_active,
            'page': self.page,
            'items': self.items,
        })

    def login_update(self, *args, data: dict, is_login: bool, **kwargs) -> None:
        self.user_update(data=data)
        if is_login:
            self.login()
        else:
            self.logout()

    def add_items(self, *args, data: list[dict], **kwargs) -> None:
        self.items = [Item(item) for item in data]

    def get_items(self) -> list[dict]:
        return [item.to_dict() for item in self.items]

    def login(self) -> None:
        self.is_login = True

    def logout(self) -> None:
        self.is_login = False

    def deactivate(self) -> None:
        self.is_active = False

    def activate(self) -> None:
        self.is_active = True

    def user_update(self, *args, data: dict, **kwargs) -> None:
        self.user = User(data)

    def account_page(self) -> None:
        self.page = 'Account'

    def store_page(self) -> None:
        self.page = 'Store'

    def main_page(self) -> None:
        self.page = 'Main'

    def sys_message_set(self, text) -> None:
        self.sys_message = text

    def sys_message_clear(self) -> None:
        self.sys_message = ''
