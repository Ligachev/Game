from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')


def get_sock_port() -> int:
    return int(config['DEFAULT']['default_port'])


def get_bind_host() -> str:
    return config['DEFAULT']['default_bind_host']


def get_client_host() -> str:
    return config['DEFAULT']['default_client_host']


def get_db_host() -> str:
    return config['DEFAULT']['db_host']


def get_db_port() -> int:
    return int(config['DEFAULT']['db_port'])


def get_start_credit() -> int:
    return int(config['DEFAULT']['credit_start'])
