"""
    ======================
    Програма-банкомат v2.3
    ======================

    Новое:
    - банкомат создается пустой, для заполнения войдите в меню икасатора
    - инкасатор может сразу заполнить банкомат набором купюр
    - у инкасатора появилась возможность посмотреть все транзакции 
      всех пользователей с отображением их логина
    - работа с базой данных

    Изменения:
    - шанс 10% получить бонус только при создании нового пользователя
    - функция check_tables_exists проверяет наличие необходимых таблиц в БД
    - учетная запись не вносится в БД
    - убрана задерка между операциями (не используется функция time.sleep)

    ======================

    В начале создается соединение с базой данных и проверяется наличие 
    еобходимых таблиц в ней.

    default_balance - стартовый баланс нового пользователя
    avialable_nominals - стартовый набор купюр для банкомата по умолчанию

    Главное меню (main_menu):
    - Вход/Регистрация
    - Выход
    Функции пользователя (user_menu):
    - Баланс
    - Транзакции
    - Пополнить
    - Снять
    - Выход
    Функции инкасатора (incasator_menu):
    - Остаток купюр
    - Транзакции
    - Пополнить
    - Загрузить стартовый набор
    - Выход
 """

import sqlite3
import os
from random import randint
from itertools import combinations
from collections import Counter

# путь расположения файлов
path = fr"{os.path.dirname(__file__)}"
# стартовый баланс нового пользователя
default_balance = 500
# логин и пароль инкасатора
inc_login = 'admin'
inc_pass = 'admin'
# стартовый набор купюр для банкомата по умолчанию
avialable_nominals = {1000: 5,
                      500: 10,
                      200: 10,
                      100: 20,
                      50: 20,
                      20: 30,
                      10: 30}
# подключаемся к БД
connect = sqlite3.connect(f'{path}/atm.db')
cursor = connect.cursor()


class LenError(Exception):
    '''Выводит сообщение, если не соблюдены ограничения длинны данных'''
    def __init__(self, field):
        self.field = field
        # если ошибка в длинне логина
        if self.field == 'Логин':
            self.message = 'От 3 до 50 символов'
        # если ошибка в длинне пароля
        elif self.field == 'Пароль':
            self.message = 'От 8 до 255 символов'


class difficultError(Exception):
    '''Выводит сообщение, если не соблюдено ограничение сложности пароля'''
    def __init__(self, value):
        self.value = value
        self.message = 'Минимум 1 {}'.format(self.value)


def check_tables_exists():
    '''Создает необходимые таблици в БД'''
    # создаем таблицу users с пользователями
    cursor.execute('CREATE TABLE IF NOT EXISTS users (\
                    id INTEGER PRIMARY KEY,\
                    login VARCHAR(50) NOT NULL,\
                    password VARCHAR(255) NOT NULL,\
                    balance INTEGER)')
    connect.commit()
    # создаем таблицу transactions со всеми транзакциями
    cursor.execute('CREATE TABLE IF NOT EXISTS transactions (\
                    id DEFAULT CURRENT_TIMESTAMP,\
                    user_id INTEGER NOT NULL,\
                    change INTEGER NOT NULL,\
                    FOREIGN KEY (user_id) REFERENCES users (id))')
    connect.commit()
    # создаем таблицу atm_bills с купюрами и их количеством в банкомате
    cursor.execute('CREATE TABLE IF NOT EXISTS atm_bills (\
                    bill INTEGER PRIMARY KEY UNIQUE,\
                    amount INTEGER)')
    connect.commit()

def main_menu():
    '''Главное меню программы'''
    print('Главное меню')
    choice = int(input('1. Вход/Регистрация\
                      \n2. Выход\n'))
    if choice == 1:
        user_authentification()
    elif choice == 2:
        print('До встречи!')
        connect.close()
        exit()
    else:
        print('Неверный выбор\n')
        main_menu()

def user_menu(login):
    '''Меню пользователя'''
    print(f'Меню {login}')
    choice = int(input('1. Баланс\
                      \n2. Транзакции\
                      \n3. Пополнить\
                      \n4. Снять\
                      \n5. Выход\n'))
    if choice == 1:
        print(f'Ваш баланс {check_balance(login)}')
        user_menu(login)
    elif choice == 2:
        limit = abs(int(input('Количество: ')))
        check_user_transactions(login, limit)
        user_menu(login)
    elif choice == 3:
        amount = abs(int(input('Сумма (целое число): ')))
        change_balance(login, amount)
        add_transaction(login, amount)
        user_menu(login)
    elif choice == 4:
        amount = abs(int(input('Сумма (целое число): ')))
        if counter(login, amount):
            change_balance(login, -amount)
            add_transaction(login, -amount)
        user_menu(login)
    else:
        print('До встречи!')
        main_menu()

def incasator_menu():
    '''Меню инкасатора'''
    print(f'Меню инкасатора')
    choice = int(input('1. Остаток купюр\
                      \n2. Транзакции\
                      \n3. Пополнить\
                      \n4. Загрузить стартовый набор\
                      \n5. Выход\n'))
    if choice == 1:
        # остаток купюр в банкомате
        incasator_menu()
    elif choice == 2:
        limit = abs(int(input('Количество: ')))
        check_all_transactions(limit)
        incasator_menu()
    elif choice == 3:
        bill = abs(int(input('Номинал купюры: ')))
        try:
            cursor.execute('SELECT bill FROM atm_bills WHERE bill = ?', (f'{bill}',))
            if bill == cursor.fetchall()[0][0]:
                amount = abs(int(input('Количество: ')))
                load_atm(bill, amount)
                incasator_menu()
        except sqlite3.ProgrammingError:
            print('Неверный номинал')
            incasator_menu()
    # обновляет содержимое банкомата до значений по умолчанию
    elif choice == 4:
        load_atm_at_start()
        incasator_menu()
    else:
        print('До встречи!')
        main_menu()

def user_authentification():
    '''Входит в аккаунт пользователя или создает нового пользователя'''
    login = input('Логин: ')
    # проверяем вход инкасатора
    if login == inc_login:
        password = input('Пароль: ')
        if password == inc_pass:
            incasator_menu()
        else:
            user_authentification()
    else:
        if login_validator(login):
            if check_users_exists(login):
                # на ввод пароля даётся 3 попытки
                attemp = 3
                while attemp > -1:
                    password = input('Пароль: ')
                    if check_user_password(login, password):
                        user_menu(login)
                    else:
                        print(f'Неверный пароль. Осталось {attemp} попыток')
                        attemp -= 1
                else:
                    print('Обратитесь в банк для восстановления пароля')
                    connect.close()
                    exit()
            else:
                password = input('Пароль: ')
                if password_validator(password):
                    add_user(login, password)
                    user_menu(login)
                else:
                    user_authentification()
        else:
            main_menu()


def check_users_exists(login):
    '''Проверяет существует ли логин'''
    cursor.execute('SELECT login FROM users WHERE login = ?', (f'{login}',))
    if cursor.fetchone():
        return True
    else:
        return False

def check_user_password(login, password):
    '''Проверяет корректность пароля по логину'''
    cursor.execute('SELECT password FROM users WHERE login = ?', (f'{login}',))
    if password == cursor.fetchall()[0][0]:
        return True
    else:
        return False

def add_user(login, password, balance=default_balance):
    '''Добавляет нового пользователя. 10% шанс получить +10 на баланс'''
    bonus = randint(1, 10)
    if bonus == 10:
        balance += bonus
        print('Поздравляем! Вам начислен бонус')
    cursor.execute('INSERT INTO users (login, password, balance) VALUES (?, ?, ?)', (f'{login}', f'{password}', balance))
    connect.commit()
    add_transaction(login, balance)

def login_validator(login):
    '''Проверяет минимальные требования к логину (длинна 3-50 символов)'''
    try:
        if len(login) < 3 or len(login) > 50:
            raise LenError('Логин')
        else:
            return True
    except LenError as err:
        print(err.message)
        return False

def password_validator(password):
    '''
    Проверяет минимальные требования к паролю:
        - длинна от 8 символов
        - минимум 1 цифра
        - минимум 1 буква в верхнем регистре
    '''
    try:
        if len(password) < 8:
            raise LenError('Пароль')
        else:
            number = 0
            upper_case = 0
            for i in password:
                if i.isdigit():
                    number += 1
                if i.isupper():
                    upper_case += 1
            if number < 1:
                raise difficultError('цифра')
            if upper_case < 1:
                raise difficultError('буква верхнего регистра')
            else:
                return True
    except LenError as err:
        print(err.message)
        return False
    except difficultError as err:
        print(err.message)
        return False

def check_balance(login):
    '''Проверить баланс пользователя'''
    cursor.execute('SELECT balance FROM users WHERE login=?', (f'{login}',))
    return cursor.fetchall()[0][0]

def change_balance(login, amount):
    '''Пополнить счет пользователя'''
    cursor.execute('UPDATE users SET balance=balance+? WHERE login=?', (f'{amount}', f'{login}'))
    connect.commit()

def add_transaction(login, amount):
    '''Добавить транзакцию пользователя'''
    cursor.execute('INSERT INTO transactions (user_id, change) VALUES (?, ?)', (get_id(login), f'{amount}'))
    connect.commit()

def check_user_transactions(login, limit):
    '''Проверить транзакции пользователя'''
    cursor.execute('SELECT id, change FROM transactions WHERE user_id=? ORDER BY transactions.id DESC LIMIT ?', (get_id(login), f'{limit}'))
    for trans in cursor.fetchall():
        print(' '.join((str(trans[0]), str(trans[1]))))

def get_id(login):
    '''Узнает id пользователя по логину'''
    cursor.execute('SELECT id FROM users WHERE login=?', (f'{login}',))
    return cursor.fetchall()[0][0]

def load_atm_at_start():
    '''Загрузить стартовый набор купюр в банкомат'''
    for key, value in avialable_nominals.items():
        cursor.execute('INSERT OR REPLACE INTO atm_bills (bill, amount) VALUES (?, ?)', (f'{key}', f'{value}'))
        connect.commit()

def check_all_transactions(limit):
    '''Проверить все транзакции в банкомате, количество строк в limit'''
    cursor.execute('SELECT transactions.id, users.login, transactions.change FROM transactions INNER JOIN users ON transactions.user_id = users.id ORDER BY transactions.id DESC LIMIT ?', (f'{limit}',))
    for trans in cursor.fetchall():
        print(' '.join((str(trans[0]), str(trans[1]), str(trans[2]))))

def load_atm(bill, amount):
    '''Загрузить банкомат, указать купюру и количество'''
    cursor.execute('UPDATE atm_bills SET amount=amount+? WHERE bill=?', (f'{amount}', f'{bill}'))
    connect.commit()

def atm_update_bills_amount(bill):
    '''Уменьшает количество определённой купюры в банкомате на 1'''
    cursor.execute('UPDATE atm_bills SET amount = amount - 1 WHERE bill = ?', (f'{bill}',))
    connect.commit()

def counter(login, amount):
    '''Подсчитывает минимальное количество купюр для выдачи'''
    # проверяем сумму на счету пользователя
    cursor.execute('SELECT balance FROM users WHERE login = ?', (f'{login}',))
    if amount > cursor.fetchone()[0]:
        print('У вас не достаточно средств')
        return False
    else:
        # создаём список всех купюр в банкомате
        cursor.execute('SELECT bill, amount FROM atm_bills')
        all_available_bills = []
        for i in cursor.fetchall():
            for j in range(i[1]):
                all_available_bills.append(int(i[0]))
        # проверяем сколько всего денег в банкомате
        max_sum = sum(all_available_bills)
        if amount > max_sum:
            print('Недостаточно денег в банкомате')
            return False
        else:
            # возможно ли выдать без остатка
            if amount % all_available_bills[0] == 0:
                # количество купюр в выдаче
                count = 0
                # все купюры в выдаче
                bills_out = []
                # находим минимально возможное количество купюр для выдачи
                for elem in range(amount // all_available_bills[-1], len(all_available_bills) + 1):
                    for combination in combinations(all_available_bills, elem):
                        if sum(combination) == amount:
                            for bill in combination:
                                count += 1
                                bills_out.append(bill)
                                atm_update_bills_amount(bill)
                            # считает сколько купюр каждого номинала мы получаем
                            nominals_out = Counter(bills_out)
                            print("Всего купюр: " + str(count))
                            for key, value in nominals_out.items():
                                print(f"{key}: {value} купюр.")
                            return True
            else:
                print(f"Минимальная купюра {all_available_bills[0]}")
                return False


if __name__ == '__main__':
    print('Добро пожаловать в DitsBank ATM')
    check_tables_exists()
    main_menu()
