import sys
from socket import AF_INET, SOCK_STREAM
import threading
import time
import json
import os
from typing import Union
from concurrent.futures import ThreadPoolExecutor

from mygame.config_parser import get_client_host, get_sock_port
from mygame.schemas import ClientStorage, User, Item
from mygame.my_socket import MySocket
from mygame.table_maker import print_table
from mygame.text_template import text_maker

BUFFER_SIZE = 4096
_thread_stop = False


def _thread_stopping() -> None:
    global _thread_stop
    _thread_stop = True


def _rendering(func=None, text=None) -> None:
    if sys.platform == 'win32':
        os.system('cls')
    if sys.platform == 'linux':
        os.system('clear')

    if func:
        func(text)


class Interface:

    def __init__(self, storage, sender, handle_storage):
        self.storage: ClientStorage = storage
        self.sender = sender
        self.handle_storage = handle_storage
        self.local = threading.local()

    def make_storage_request(
            self,
            executor: dict = None,
            field: str | bool = None
    ) -> Union[User | bool | str | list[dict]]:
        with ThreadPoolExecutor(1) as pool_executor:
            while True:
                if executor and field:
                    method = 'get execute'
                    pool = pool_executor.submit(self.handle_storage, method, {'func': executor['func']})
                    feature = pool.result()
                    return feature
                elif executor:
                    method = 'execute'
                    thread_exec = threading.Thread(
                        target=self.handle_storage,
                        args=(method, {'func': executor['func']}),
                        daemon=True
                    )
                    thread_exec.start()
                    break
                elif field:
                    method = 'get'
                    pool = pool_executor.submit(self.handle_storage, method, {'field': field})
                    feature = pool.result()
                    return feature

    def run(self) -> None:
        while not _thread_stop:
            self.make_storage_request(executor={'func': self.storage.activate})
            while self.make_storage_request(field='is_active'):
                try:
                    _rendering(self.registration, text_maker('Registration'))
                    self.sys_mg()
                    while self.make_storage_request(field='is_login'):
                        page = self.make_storage_request(field='page')
                        match page:
                            case 'Main':
                                _rendering(self.main_menu, text_maker(page))
                            case 'Account':
                                _rendering(self.account, text_maker(page))
                            case 'Store':
                                _rendering(self.store, text_maker(page))
                except (EOFError, KeyboardInterrupt):
                    self.routing('exit')

    def sys_mg(self):
        sys_mg = self.make_storage_request(field='sys_message')
        if sys_mg:
            _rendering(self.print_sys_mg, sys_mg)
            self.make_storage_request(executor={'func': self.storage.sys_message_clear})

    @staticmethod
    def print_sys_mg(sys_mg):
        print(sys_mg)
        time.sleep(1)

    def routing(self, root: str) -> str | None:
        switch_commands = {
            'exit': [_thread_stopping, self.storage.deactivate, self.storage.logout, self.storage.main_page],
            'logout': [self.storage.logout, self.storage.main_page],
            'account': [self.storage.account_page],
            'store': [self.storage.store_page],
            'main': [self.storage.main_page],
            'state': [self.storage.print_store],
        }
        commands = switch_commands.get(root.lower())

        if not commands:
            return root

        for command in commands:
            self.make_storage_request(executor={'func': command})

        return

    def registration(self, text) -> None:
        name = input(text)
        if name == 'exit':
            self.routing(name)
            return
        params = {
            "function": "login",
            "data": {
                "name": name,
            }
        }
        self.sender(params)

    def main_menu(self, text: str) -> None:
        root = self.routing(input(text))
        if root is None:
            return

    def account(self, text: str) -> None:
        user = self.make_storage_request(field='user')
        print(text[0].format(user.name, user.credit))
        items = user.get_items()

        if len(items) > 0:
            print_table(data=items)
        else:
            print(text[1])
        inp = self.routing(input(text[2]))
        if not inp:
            return
        if inp.lower() == 'top up':
            self.top_up()
            self.sys_mg()
            return
        else:
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
            self.sys_mg()

    def store(self, text: str) -> None:
        print(text[0])
        items: list[dict] = self.make_storage_request(
            field=True,
            executor={'func': self.storage.get_items}
        )
        if not items:
            self.get_items(text[1])
            self.sys_mg()
            return
        print_table(data=items)

        inp = self.routing(input(text[2]))
        if not inp:
            return
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
        self.sys_mg()

    def top_up(self):
        while True:
            try:
                payment = int(input(text_maker('Top up')))
            except ValueError:
                print(text_maker('ValueError'))
            else:
                break
        params = {
            'function': 'top_up',
            'data': {
                'name': self.make_storage_request(field='user').name,
                'credit': payment,
            },
        }
        self.sender(params)

    def sell_items(self, item_ids: list[int]):
        params = {
            'function': 'sell_items',
            'data': {
                'name': self.make_storage_request(field='user').name,
                'item_ids': item_ids,
            },
        }
        self.sender(params)

    def buy_items(self, item_ids: list[int]):
        params = {
            'function': 'buy_items',
            'data': {
                'name': self.make_storage_request(field='user').name,
                'item_ids': item_ids,
            },
        }
        self.sender(params)

    def get_items(self, text):
        print(text)
        params = {
            "function": "get_items",
        }
        self.sender(params)


class ClientServer:
    def __init__(self, socket):
        self.socket: MySocket = socket
        self.storage: ClientStorage = ClientStorage(is_login=False, is_active=False, page='Main')
        self.is_response: bool = False

    def run_client(self):
        listener_thr = threading.Thread(target=self.listener, daemon=True)
        interface = Interface(self.storage, self.sender, self.handle_storage)
        listener_thr.start()
        interface.run()
        listener_thr.join(timeout=1)
        _rendering()

    def handle_storage(self, method: str | bool, data_dict: dict) -> Union[User | bool | str | list[Item]] | None:
        locker = threading.RLock()
        with locker:
            match method:
                case 'get execute':
                    func = data_dict.get('func')
                    return func() if func else []
                case 'get':
                    return self.storage_mapping(data_dict)
                case 'execute':
                    data_dict.get('func')()
                case 'update':
                    print('\n\n\n>>>System message<<<:', data_dict['System message'], '\n\n\n')
                    self.task_mapping(data_dict)
                case _:
                    return

    def sender(self, params: dict):
        with ThreadPoolExecutor(1) as pool_executor:
            pool = pool_executor.submit(self.send, params)
            pool.result()

    def send(self, request: dict) -> None:
        try:
            self.socket.send(json.dumps(request).encode(encoding='utf-8'))
            self.is_response = False
            while not self.is_response:
                pass

        except ConnectionError:
            print(f"Client suddenly closed while receiving")

    def listener(self) -> None:
        global _thread_stop
        while not _thread_stop:
            try:
                bin_arr = self.socket.recv_msg()
                data_json = json.loads(bin_arr)
                self.handle_storage('update', data_json)
                self.is_response = True
            except (ConnectionError, ConnectionAbortedError):
                if _thread_stop:
                    break
                continue

    def storage_mapping(self, store: dict) -> Union[User | bool | str | list[Item]]:
        field = store.get('field')
        return self.storage[field]

    def task_mapping(self, data_json):
        func = data_json.get('function')
        data = data_json.get('data')
        sys_message = data_json.get('System message')
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
        if sys_message:
            message = text_maker('System message')
            self.storage.sys_message_set(message.format(sys_message))


if __name__ == "__main__":
    with MySocket(AF_INET, SOCK_STREAM) as sock:
        sock.connect((get_client_host(), get_sock_port()))
        server = ClientServer(sock)
        server.run_client()
        sock.close()
