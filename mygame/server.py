from socket import socket, AF_INET, SOCK_STREAM
from concurrent.futures import ThreadPoolExecutor
import struct
import json
import selectors
from mygame.database import MongoDB
from mygame.config_parser import get_bind_host, get_sock_port
from mygame.text_template import system_message_creator
from mygame.schemas import Item


BUFFER_SIZE = 4096
ENCODING = 'utf-8'


def user_login(mongo: MongoDB, data: dict) -> dict:
    user = mongo.find_user(data['name'])
    if user.id is not None:
        return {'function': 'login', 'status': 'succeeded', 'data': user.to_dict(), 'is_login': True}
    else:
        try:
            new_user = mongo.create_user(data['name'])
        except Exception:
            return {'function': 'login_new_user', 'status': 'failed', 'is_login': False}
        else:
            return {'function': 'login_new_user', 'status': 'succeeded', 'data': new_user.to_dict(), 'is_login': True}


def get_items(mongo: MongoDB, **kwargs) -> dict:
    items = mongo.find_items()
    if len(items) > 0:
        return {'function': 'get_items', 'status': 'succeeded', 'data': items}
    else:
        return {'function': 'get_items', 'status': 'failed', 'data': []}


def buy_items(mongo: MongoDB, data: dict):
    items = mongo.find_items()
    user = mongo.find_user(data['name'])
    for_pay = []
    total_price = 0
    for item in items:
        if item['id'] in data['item_ids']:
            for_pay.append(item)
            total_price += item['price']

    credit = user.credits() - total_price
    if credit < 0:
        return {'function': 'buy_items', 'status': 'failed', 'data': user.to_dict()}
    else:
        user.update_items(user.items + [Item(item) for item in for_pay])
        user.credits_update(credit)
        mongo.update_user(user.to_dict())
        return {'function': 'buy_items', 'status': 'succeeded', 'data': user.to_dict()}


def sell_items(mongo: MongoDB, data: dict):
    user = mongo.find_user(data['name'])
    for_sail = []
    total_price = 0
    items = user.get_items()
    if len(items) == 0:
        return {'function': 'sell_items', 'status': 'failed', 'data': user.to_dict()}
    for item in items:
        if item['id'] not in data['item_ids']:
            for_sail.append(item)
            continue
        total_price += item['price']

    credit = user.credits() + total_price
    user.update_items([Item(item) for item in for_sail])
    user.credits_update(credit)
    mongo.update_user(user.to_dict())
    return {'function': 'sell_items', 'status': 'succeeded', 'data': user.to_dict()}


def top_up(mongo: MongoDB, data: dict):
    user = mongo.find_user(data['name'])
    try:
        credit = user.credits() + data['credit']
        user.credits_update(credit)
        mongo.update_user(user.to_dict())
        return {'function': 'top_up', 'status': 'succeeded', 'data': user.to_dict()}
    except Exception:
        return {'function': 'top_up', 'status': 'failed', 'data': user.to_dict()}


_func_mapping = {
    'login': user_login,
    'get_items': get_items,
    'buy_items': buy_items,
    'sell_items': sell_items,
    'top_up': top_up,
}


class TaskManager:
    tasks: list = []

    def __init__(self):
        self.mongo: MongoDB = MongoDB()

    def add_task(self, task: dict):
        self.tasks.append(task)

    def run_task(self):
        task_result = []
        for i in range(len(self.tasks), 0, -1):
            task = self.tasks.pop(i-1)
            func = task.get('function')
            data = task.get('data')
            task_result.append(_func_mapping[func](
                self.mongo,
                data=data,
            ))

        return task_result


class Server:

    def __init__(self, serv_socket):
        self.socket: socket = serv_socket
        self.task_manager: TaskManager = TaskManager()
        self.pool: ThreadPoolExecutor = ThreadPoolExecutor()

    @staticmethod
    def sender(client_socket, feature) -> bool:
        try:
            for result in feature:
                sys_message = system_message_creator(result)
                message = sys_message | result
                data = json.dumps(message, indent=4).encode(ENCODING)
                msg = struct.pack('>I', len(data)) + data
                print('Отправка данных: ', data)
                client_socket.send(msg)

        except ConnectionError:
            print(f"Клиент внезапно закрылся, не может быть отправлено")
            return False
        return True

    def handle_client(self, client_socket, address: tuple) -> bool:
        while True:
            try:
                data = client_socket.recv(BUFFER_SIZE)
            except (ConnectionError, ConnectionAbortedError):
                print(f"Клиент прервал соединение в процессе передачи данных")
                return False

            try:
                data_json = json.loads(data)
            except json.JSONDecodeError:
                return False

            if not data_json:
                print("Отключено пользователем", address)
                return False

            self.task_manager.add_task(data_json)
            feature = self.pool.submit(self.task_manager.run_task)
            feature_result = feature.result()

            self.sender(client_socket, feature_result)

            return True

    def run_server(self):

        def get_connect(sel, serv_sock):
            sock, addr = serv_sock.accept()
            sel.register(sock, selectors.EVENT_READ, get_request)
            print("Установленно соединение", addr, sock)

        def get_request(sel, sock):
            addr = sock.getpeername()
            if not self.handle_client(sock, addr):
                sel.unregister(sock)
                sock.close()

        self.socket.listen(10)
        sel = selectors.DefaultSelector()
        sel.register(self.socket, selectors.EVENT_READ, get_connect)
        while True:
            print("Ожидаю входящее соединение или данные...")
            events = sel.select()
            for key, _ in events:
                callback = key.data
                callback(sel, key.fileobj)


if __name__ == "__main__":
    with socket(AF_INET, SOCK_STREAM) as sock:
        sock.bind((get_bind_host(), get_sock_port()))
        server = Server(sock)
        server.run_server()

