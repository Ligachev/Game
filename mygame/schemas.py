class ClientStorage:

    def __init__(self, is_login: bool, is_active: bool, page: str):
        self.user: dict
        self.is_login: bool = is_login
        self.is_active: bool = is_active
        self.page: str = page
        self.items: list[dict] = []
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
            'user': self.user,
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
        self.items = data

    def get_items(self) -> list[dict]:
        return self.items

    def login(self) -> None:
        self.is_login = True

    def logout(self) -> None:
        self.is_login = False

    def deactivate(self) -> None:
        self.is_active = False

    def activate(self) -> None:
        self.is_active = True

    def user_update(self, *args, data: dict, **kwargs) -> None:
        self.user = data

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
