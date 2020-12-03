"""
    ======================
    Програма-банкомат v2.2
    ======================

    Нове:
    - кожна авторизація користувача (log_in) дає йому 10% шанс
      отримати бонус на рахунок (не доступно для інкасатора)
    - у транзакціях вказується сумма, на яку змінився баланс

    Зміни:
    - перевірка наявності усіх необхідних директорій та файлів
      винесена в окрему функцію (dir_checker)
    - користувачі зберігаються у файлі users.csv
    - транзакції зберігаються в форматі .csv
    - ID транзакції відображається у форматі дати та часу операції

    В розробці:
    - оптимізація та усунення недоліків алгоритму видачі купюр
      (з ростом кількості купюр для видачі збільшується час на
      виконання алгоритму)

    ======================

    На початку створює/перевіряє наявність усіх необхідних директорій
    та файлів (users.csv, <balance>, <transactions>) та створюється
    обліковий запис інкасатора (inc_name, inc_pass)

    default_money - стартовий капітал нового користувача
    avialable_nominals - доступні номінали та їх стартова кількість

    Головне меню (start):
    - увійти (log_in)
    - новий користувач (new_user)
    - вихід
    Доступні функції (operations):
    - перевірити баланс (balance)
    - покласти гроші (deposit)
    - зняти гроші (withdraw)
    - історія балансу (history)
    - вихід
    Функції інкасатора (incasator_menu):
    - залишок купюр
    - поповнити банкомат (load_atm)
    - вихід
 """

import csv
import json
import os
import time
import datetime
from random import randint
from itertools import combinations
from collections import Counter

# default incasator name
inc_name = "incasator"
# default incasator password
inc_pass = "ilovemono"
# set start deposit
default_money = 1000.0
# set default nominals in ATM
avialable_nominals = {1000: 5,
                      500: 10,
                      200: 10,
                      100: 20,
                      50: 20,
                      20: 30,
                      10: 30}

path = fr"{os.path.dirname(__file__)}"


class lenError(Exception):
    def __init__(self, length, field):
        if field == "Login":
            length = "from 3 to 50"
        if field == "Password":
            length = "at least 8"
        self.length = length
        self.field = field


class difficultError(Exception):
    def __init__(self, value):
        self.value = value


def start():
    """
    main menu of ATM
    """
    print("MAIN MENU")
    choice = input("1. LogIn \n2. Create account \n3. Exit\n")
    if choice == "1":
        log_in()
    elif choice == "2":
        new_user()
    elif choice == "3":
        print("GOODBYE!")
        time.sleep(2)
        exit()
    else:
        print("Wrong option!\n")
        start()


def dir_checker():
    """
    checking if all necessary directories exists
    """
    if not os.path.exists(f"{path}/transactions/"):
        os.mkdir(f"{path}/transactions")
    if not os.path.exists(f"{path}/balance/"):
        os.mkdir(f"{path}/balance")
    if not os.path.exists(f"{path}/users.csv"):
        with open(f"{path}/users.csv", "w", encoding="utf-8", newline="") as f:
            fields = ["Login", "Password"]
            file_writer = csv.DictWriter(f, delimiter=",", fieldnames=fields)
            file_writer.writeheader()
            file_writer.writerow({"Login": inc_name, "Password": inc_pass})
    if not os.path.exists(f"{path}/ATM_cash.json"):
        with open(f"{path}/ATM_cash.json", "w") as f:
            json.dump(avialable_nominals, f)
    return


def login_validator(login):
    """
    checking minimum requirements for login
    """
    try:
        if len(login) < 3 or len(login) > 50:
            raise lenError(len(login), "Login")
        else:
            return True
    except lenError as err1:
        print("{} length must be {} characters"
              .format(err1.field, err1.length))
        return False


def password_validator(password):
    """
    checking minimum requirements for password
    """
    try:
        if len(password) < 8:
            raise lenError(len(password), "Password")
        else:
            number = 0
            upper_case = 0
            for i in password:
                if i.isdigit():
                    number += 1
                if i.isupper():
                    upper_case += 1
            if number < 1:
                raise difficultError("digit")
            if upper_case < 1:
                raise difficultError("upper case letter")
            else:
                return True

    except lenError as err1:
        print("{} length must be {} characters"
              .format(err1.field, err1.length))
        return False
    except difficultError as err2:
        print("Password must have at least 1 {}".format(err2.value))
        return False


def log_in():
    """
    cheking if login/password are correct
    """
    with open(f"{path}/users.csv", encoding="utf-8") as f:
        f.readline()
        file_reader = csv.reader(f, delimiter=",")
        login = input("Login: ")
        for row in file_reader:
            if login == row[0]:
                # change number of attemps (att) to input password
                att = 3
                i = 0
                while i < att:
                    password = input("Password: ")
                    if password == row[1]:
                        print(f"Welcome, {login}\n")
                        bonus = randint(1, 10)
                        time.sleep(1)
                        operations(login, bonus)
                    else:
                        print(f"WRONG PASSWORD. You have {att - i} attemps:")
                        i += 1
                else:
                    print("WRONG PASSWORD")
                    time.sleep(1)
                    print("Contact your bank manager for more information")
                    exit()
            else:
                continue
        else:
            print("User not found\n")
            time.sleep(1)
            start()


def new_user():
    """
    creating new account if user is not in <users.csv>
    """
    print("CREATE NEW ACCOUNT\n")
    login = input("Login: ")
    if login_validator(login):
        with open(f"{path}/users.csv", encoding="utf-8") as f:
            f.readline()
            file_reader = csv.reader(f, delimiter=",")
            for row in file_reader:
                if login == row[0]:
                    print("This user already exists")
                    time.sleep(2)
                    start()
                else:
                    password = input("Password: ")
                    if password_validator(password):
                        # set default balance and add first line to history
                        with open(f"{path}/users.csv", mode="a",
                                  encoding="utf-8", newline="") as f:
                            file_writer = csv.writer(f, delimiter=",")
                            file_writer.writerow([login, password])
                            print(f"Welcome, {login}\n")
                        with open(f"{path}/balance/{login}_balance.txt",
                                  "w") as bal:
                            bal.write(str(float(default_money)))
                        with open(f"{path}/transactions/{login}_history.csv",
                                  "w", encoding="utf-8", newline="") as f:
                            fields = ["Date", "Change", "Balance"]
                            file_writer = csv.DictWriter(f, delimiter=",",
                                                         fieldnames=fields)
                            file_writer.writeheader()
                            now = datetime.datetime.now()
                            a = now.strftime("%d-%m-%Y %H:%M:%S")
                            file_writer.writerow({"Date": a,
                                                  "Change": default_money,
                                                  "Balance": default_money})
                        time.sleep(1)
                        operations(login)
                    else:
                        new_user()
    else:
        new_user()


def operations(login, bonus=0):
    """
    menu for all avialable operations.
    incasator is redirecting to hiden incasator menu
    """
    print("OPERATIONS")
    if login == inc_name:
        incasator_menu(login)
    else:
        if bonus == 10:
            print("!!! YOU WIN 10$ BONUS !!!")
            with open(f"{path}/balance/{login}_balance.txt") as f:
                new_bal = 10 + float(f.read())
            with open(f"{path}/balance/{login}_balance.txt", "w") as f:
                f.write(str(new_bal))
            transactions(login, bonus, new_bal)
            time.sleep(1)
        choice = int(input(
            "1. Balance \n2. Deposit \n3. Withdraw\n4. History\n5. Exit\n"))
        if choice == 1:
            balance(login)
        elif choice == 2:
            deposit(login)
        elif choice == 3:
            withdraw(login)
        elif choice == 4:
            history(login)
        elif choice == 5:
            print(f"Goodbye, {login}!")
            time.sleep(2)
            start()
        else:
            print("Wrong option\n")
            operations(login)


def incasator_menu(login):
    """
    menu with incasator commands
    """
    choice = int(input("1. Check ATM\n2. Load ATM\n3. Exit\n"))
    if choice == 1:
        with open(f"{path}/ATM_cash.json") as f:
            cash = json.load(f)
        all_bills = []
        for bills in cash:
            for bill in range(cash[bills]):
                all_bills.append(int(bills))
        max_sum = sum(all_bills)
        print("ATM cash: " + str(max_sum) + "$")
        for k, v in cash.items():
            print(f"{k}$: {v}")
        time.sleep(2)
        incasator_menu(login)
    elif choice == 2:
        load_atm(login)
        incasator_menu(login)
    elif choice == 3:
        print(f"Goodbye, {login}!")
        time.sleep(1)
        start()
    else:
        print("Wrong option\n")
        incasator_menu(login)


def load_atm(login):
    """
    loading ATM with avialable nominals
    """
    with open(f"{path}/ATM_cash.json") as f:
        cash = json.load(f)
    nominal = str(input("Enter nominal: "))
    if nominal in cash:
        amount = int(input("Amount: "))
        cash[nominal] = amount + cash[nominal]
    else:
        print("Wrong nominal\n")
        time.sleep(1)
        load_atm(login)
    with open(f"{path}/ATM_cash.json", "w") as f:
        json.dump(cash, f)
    choice = input("Done. Load more? y/n: ")
    if choice == "y":
        load_atm(login)
    elif choice == "n":
        incasator_menu(login)
    else:
        print("Wrong option\n")
        time.sleep(1)
        incasator_menu(login)


def balance(login):
    """
    checkin user balance
    """
    with open(f"{path}/balance/{login}_balance.txt") as f:
        bal = round(float(f.read()), 2)
        print("Your balance is: " + str(bal) + "$")
        time.sleep(2)
        operations(login)


def deposit(login):
    """
    deposit money to account
    """
    try:
        depo = input("Amount: ")
        if float(depo) <= 0:
            print("More than 0")
            time.sleep(1)
            deposit(login)
        else:
            with open(f"{path}/balance/{login}_balance.txt") as f:
                new_bal = float(depo) + float(f.read())
            with open(f"{path}/balance/{login}_balance.txt", "w") as f:
                f.write(str(new_bal))
                transactions(login, depo, new_bal)
            print("Done")
            time.sleep(1)
            operations(login)
    except ValueError:
        print("Only numbers")
        deposit(login)


def withdraw(login):
    """
    widthraw money from ATM
    """
    try:
        withdr = abs(int(input("Amount: ")))
        if withdr == 0:
            print("More than 0")
            time.sleep(1)
            withdraw(login)
        else:
            with open(f"{path}/balance/{login}_balance.txt") as f:
                new_bal = float(f.read()) - float(withdr)
                if new_bal < 0:
                    print("Not enough money")
                    withdraw(login)
                else:
                    if counter(withdr):
                        with open(
                            f"{path}/balance/{login}_balance.txt", "w"
                        ) as f:
                            f.write(str(new_bal))
                            change = 0 - withdr
                            transactions(login, change, new_bal)
                        print("Done")
                        time.sleep(1)
                        operations(login)
                    else:
                        withdraw(login)
    except ValueError:
        print("Only integer numbers")
        withdraw(login)


def counter(withdr):
    """
    cheking if it is possible to withdraw from ATM
    """
    with open(f"{path}/ATM_cash.json") as f:
        cash = json.load(f)
    all_bills = []
    bills_out = []
    for bills in cash:
        for bill in range(cash[bills]):
            all_bills.append(int(bills))
    max_sum = sum(all_bills)
    if withdr > max_sum:
        print(f"Not enough money in ATM. Maximum is {max_sum}")
        return False
    else:
        # checking minimal bill in ATM
        if withdr % all_bills[-1] == 0:
            count = 0
            for i in range(withdr // all_bills[0], len(all_bills) + 1):
                for c in combinations(all_bills, i):
                    if sum(c) == withdr:
                        for i in c:
                            count += 1
                            bills_out.append(i)
                            cash[str(i)] -= 1
                        # count how many bills of each nominal we used
                        nominals_out = Counter(bills_out)
                        print("Total bills: " + str(count))
                        for key, value in nominals_out.items():
                            print(f"{key}: {value} bills.")
                        with open(f"{path}/ATM_cash.json", "w") as f:
                            json.dump(cash, f)
                        return True
        else:
            print(f"Sorry, but minimum bill is {all_bills[-1]}")
            return False


def transactions(login, amount, balance):
    with open(f"{path}/transactions/{login}_history.csv", "a",
              encoding="utf-8", newline="") as f:
        file_writer = csv.writer(f, delimiter=",")
        now = datetime.datetime.now()
        a = now.strftime("%d-%m-%Y %H:%M:%S")
        file_writer.writerow([a, amount, balance])


def history(login):
    with open(f"{path}/transactions/{login}_history.csv",
              encoding="utf-8") as f:
        f.readline()
        file_reader = csv.reader(f, delimiter=",")
        for row in file_reader:
            print(*row)
        time.sleep(2)
        operations(login)


if __name__ == "__main__":
    print("WELCOME TO GeeK-BANK\n")
    time.sleep(1)
    dir_checker()
    start()
