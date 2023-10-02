def text_maker(root: str) -> str:
    switch_text = {
        'System message': '\n\n\n\n\t\t\t>>>System message<<<:\t {}',
        'Registration': '\n\n\n\n\n\n\n\t\t\t\t\t<<<Добро пожаловать в СУПЕР ИГРУ!!!!>>>'
                        '\n\n\n\n\n\n\n\nДля продолжения, введите ЛОГИН ПОЛЬЗОВАТЕЛЯ или введите Exit для завершения программы: \n>>>_',
        'Main': '\n\n\n\n\n\n\n\t\t\t\t\t<<<Добро пожаловать в главное меню>>>'
                '\n\n\n\n\n\n\n\nДля перемещения по приложению используйте команды: Logout, Account, Store, Exit, State: \n>>>_',
        'Account': [
            '\n\n\n\n\n\n\n\t\t\t\t\t<<<Добро пожаловать в игровой аккаунт {}>>>'
            '\n\n\t\t\t\t\t<<<Ваш игровой баланс {} кредитов>>>\n\n\n\n\n',
            '\n\t\n\t\t<<<Вы не имеете игровых покупок, покупки можно совершить в магазине игры>>>',
            '\n\n\n\n\n\n\n\nДля продажи, укажите ID одного или нескольких товаров.'
            '\nЧто бы пополнить баланс введите команду "top up".'
            '\nДля перемещения по приложению используйте команды: Logout, Account, Main, Store, Exit, State:\n>>>_',
            '\nВы желаете продать {} items, на общую сумму {} кредитов.'
            '\nYes/No:\n>>>_',
        ],
        'Top up fake': 'Пополнить баланс можно только в личном кабинете',
        'Top up': '\nУкажите сумму пополнения:\n>>>_',
        'ValueError': '<<<!!!!!!!Введите цифру!!!!!!!>>>',
        'Store': [
            '\n\n\n\n\n\n\n\t\t\t\t\t<<<Добро пожаловать в магазин>>>\n\n\n\n\n\n\n\t\t\t\t\t',
            '<<<Ожидайте выполняется загрузка магазина>>>',
            '\n\n\n\n\n\n\n\nДля покупки, укажите ID одного или нескольких товаров.'
            '\nДля перемещения по приложению используйте команды: Logout, Account, Main, Exit, State:\n>>>_',
            '\nВы желаете купить {} items, на общую сумму {} кредитов.'
            '\nYes/No:\n>>>_'
        ],
    }
    return switch_text.get(root)


def system_message_creator(download: dict) -> dict:
    func = download.get('function')
    status = download.get('status')
    data = download.get('data')
    name = data.get('name') if isinstance(data, dict) else ''
    credit = data.get('credit') if isinstance(data, dict) else ''
    items = data if isinstance(data, list) else []
    template_message = {
        'succeeded': {
            'login': f'Welcome {name}!',
            'login_new_user': f'Welcome {name}! '
                              f'you received a welcome bonus {credit} credits.',
            'get_items': f'The store was loaded successfully! Number of available items: {len(items)}.',
            'buy_items': 'Purchase completed successfully',
            'sell_items': 'Sale completed successfully',
            'top_up': 'Purchase completed successfully',
        },
        'failed': {
            'login_new_user': f'Hello {name}, We have som technical problems.',
            'get_items': 'An error occurred while loading the store.',
            'buy_items': 'There are insufficient credits in your account.',
            'sell_items': 'Transaction processing error',
            'top_up': 'Transaction processing error',
        }
    }
    return {'System message': template_message[status][func]}