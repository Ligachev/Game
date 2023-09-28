from socket import AF_INET, SOCK_STREAM
import threading
import time
import json

from mygame.config_parser import get_client_host, get_sock_port
from mygame.schemas import ClientStorage
from mygame.my_socket import MySocket
from mygame.table_maker import print_table
from mygame.text_template import text_maker

BUFFER_SIZE = 4096
_thread_stop = False


class Interface:

    def __init__(self, socket, storage, sendr, thread_stopping):
        self.storage: ClientStorage = storage
        self.socket: MySocket = socket
        self.sender = sendr
        self.thread_stopping = thread_stopping

    def run(self) -> None:
        while self.storage.is_active:
            try:
                self.registration(text_maker('Registration'))
                while self.storage.is_login:
                    main = 'Main'
                    store = 'Store'
                    account = 'Account'
                    if self.storage.page == account:
                        self.account(text_maker(account))
                    elif self.storage.page == store:
                        self.store(text_maker(store))
                    elif self.storage.page == main:
                        self.main_menu(text_maker(main))
            except (EOFError, KeyboardInterrupt):
                self.routing('exit')

    def routing(self, root: str) -> str | None:
        switch_commands = {
            'exit': [self.thread_stopping, self.storage.deactivate, self.storage.logout, self.storage.main_page],
            'logout': [self.storage.logout, self.storage.main_page],
            'account': [self.storage.account_page],
            'store': [self.storage.store_page],
            'main': [self.storage.main_page],
            'state': [self.storage.print_store],
            'top up': [self.top_up],
        }
        commands = switch_commands.get(root.lower())

        if not commands:
            return root

        for command in commands:
            if commands == 'top up' and self.storage.page != 'account':
                print(text_maker('Top up fake'))
                return command

            command()

        return

    def registration(self, text) -> None:
        name = input(text)
        if name == 'exit':
            self.routing(name)
            return
        self.sender({
            "function": "login",
            "data": {
                "name": name,
            }
        }
        )
        time.sleep(1)

    def main_menu(self, text: str) -> None:
        while True:
            root = self.routing(input(text))
            if root is None:
                return

    def account(self, text: str) -> None:
        print(text[0].format(self.storage.user.name, self.storage.user.credit))
        items = self.storage.user.get_items()
        if len(items) > 0:
            print_table(data=items)
        else:
            print(text[1])

        while self.storage.page == 'Account':
            inp = self.routing(input(text[2]))
            if not inp:
                break
            item_ids = []
            for char in inp.split(','):
                try:
                    item_ids.append(int(char))
                except ValueError:
                    print(text_maker('ValueError'))
                    return

            price = [item['price'] for item in items if item['id'] in item_ids]

            ask = input(text[3].format(len(item_ids), sum(price)))

            if ask.lower() == 'yes':
                self.sell_items(item_ids)

    def store(self, text: str) -> None:
        print(text[0])
        items = self.storage.get_items()
        if not items:
            self.get_items(text[1])
            items = self.storage.get_items()
        print_table(data=items)
        while self.storage.page == 'Store':
            inp = self.routing(input(text[2]))
            if not inp:
                break
            inp = inp.split(',')
            item_ids = []
            for char in inp:
                try:
                    item_ids.append(int(char))
                except ValueError:
                    print(text_maker('ValueError'))
                    return

            price = [item['price'] for item in items if item['id'] in item_ids]
            ask = input(text[3].format(len(item_ids), sum(price)))

            if ask.lower() == 'yes':
                self.buy_items(item_ids)

    def top_up(self):
        while True:
            try:
                payment = int(input(text_maker('Top up')))
            except ValueError:
                print(text_maker('ValueError'))
            else:
                break

        self.sender({
            'function': 'top_up',
            'data': {
                'name': self.storage.user.name,
                'credit': payment,
            },
        }
        )
        time.sleep(1)

    def sell_items(self, item_ids: list[int]):
        self.sender({
            'function': 'sell_items',
            'data': {
                'name': self.storage.user.name,
                'item_ids': item_ids,
            },
        }
        )
        time.sleep(1)

    def buy_items(self, item_ids: list[int]):
        self.sender({
            'function': 'buy_items',
            'data': {
                'name': self.storage.user.name,
                'item_ids': item_ids,
            },
        }
        )
        time.sleep(1)

    def get_items(self, text):
        print(text)
        self.sender({
            "function": "get_items",
        }
        )
        time.sleep(1)


class ClientServer:
    def __init__(self, socket):
        self.socket: MySocket = socket
        self.storage = ClientStorage(is_login=False, is_active=True, page='Main')

    def run_client(self):
        interface = Interface(self.socket, self.storage, self.sender, self.thread_stopping)
        listener = self.listener()
        print('listener')
        interface.run()
        listener.join(timeout=1)

    def sender(self, request: dict) -> None:
        try:
            self.socket.send(json.dumps(request).encode(encoding='utf-8'))

        except ConnectionError:
            print(f"Client suddenly closed while receiving")

    def thread_stopping(self):
        global _thread_stop
        _thread_stop = True

    def listener(self):
        socket = self.socket
        task_mapping = self.task_mapping

        class Listener(threading.Thread):
            def run(self) -> None:
                global _thread_stop
                while not _thread_stop:
                    try:
                        bin_arr = socket.recv_msg()
                        data_json = json.loads(bin_arr)
                        print('\n\n\n>>>System message<<<:', data_json['System message'], '\n\n\n')
                        task_mapping(data_json)
                    except (ConnectionError, ConnectionAbortedError):
                        if _thread_stop:
                            break
                        continue

        listener = Listener(daemon=True)
        listener.start()

        return listener

    def task_mapping(self, data_json):
        func = data_json.get('function')
        data = data_json.get('data')
        # status = json.get('status')
        is_login = data_json.get('is_login')
        func_mapping = {
            'login': self.storage.login_update,
            'login_new_user': self.storage.login_update,
            'get_items': self.storage.add_items,
            'buy_items': self.storage.user_update,
            'sell_items': self.storage.user_update,
            'top_up': self.storage.user_update,
        }
        func_mapping[func](data=data, is_login=is_login)


if __name__ == "__main__":
    with MySocket(AF_INET, SOCK_STREAM) as sock:
        sock.connect((get_client_host(), get_sock_port()))
        server = ClientServer(sock)
        server.run_client()
        sock.close()
