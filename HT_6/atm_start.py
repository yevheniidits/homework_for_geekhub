"""
    Програма-банкомат v2.1
    Нові функції:
        - при створенні новго користувача, перевіряється відповідність
          логіну і паролю мінімальним вимогам
          (login_validator, password_validator)
        - покласти на рахунок можна будь-яку сумму, але це не впливає
          на залишок купюр в банкоматі
        - видача купюр здійснюється за логікою видачі найменшої кількості
          купюр. Враховані недоліки "жадібного" алгоритму

    На початку створює/перевіряє наявність усіх необхідних директорій
    та файлів (users.json, <balance>, <transactions>) та створюється
    обліковий запис інкасатора (incasator_name, incasator_pass)

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


import json
import os
import time
from itertools import combinations
from collections import Counter

# default incasator name
incasator_name = "incasator"
# default incasator password
incasator_pass = {"password": "ilovemono"}
# set start deposit
default_money = 1000
# set default nominals in ATM
avialable_nominals = {1000: 10,
                      500: 20,
                      200: 30,
                      100: 40,
                      50: 50,
                      20: 100,
                      10: 100}

path = fr'{os.path.dirname(__file__)}'


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


# main menu of ATM
def start():
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


# checking minimum requirements for login
def login_validator(login):
    try:
        if len(login) < 3 or len(login) > 50:
            raise lenError(len(login), "Login")
        else:
            return True
    except lenError as err1:
        print("{} length must be {} characters"
              .format(err1.field, err1.length))
        return False


# checking minimum requirements for password
def password_validator(password):
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


# cheking if login/password are correct
def log_in():
    with open(fr"{path}/users.json") as f:
        all_users = json.load(f)
    login = input("Login: ")
    if login in all_users:
        check_pass = all_users[login]
        # change number of attemps (att) to input password
        att = 3
        i = 0
        while i < att:
            password = input("Password: ")
            if password == check_pass["password"]:
                print(f"Welcome, {login}\n")
                time.sleep(1)
                operations(login)
            else:
                print(f"WRONG PASSWORD. You have {att - i} attemps:")
                i += 1
        else:
            print("WRONG PASSWORD")
            time.sleep(1)
            print("Contact your bank manager for more information")
            exit()
    else:
        print("User not found\n")
        time.sleep(1)
        start()


# creating new account if user is not in <users.json>
def new_user():
    print("CREATE NEW ACCOUNT\n")
    with open(fr"{path}/users.json") as f:
        all_users = json.load(f)
    login = input("Login: ")
    if login_validator(login):
        if login in all_users:
            print("This user already exists")
            time.sleep(2)
            start()
        else:
            password = input("Password: ")
            if password_validator(password):
                new_pass = {"password": password}
                all_users[login] = new_pass
                # set default balance and add first line to history
                with open(fr"{path}/users.json", "w") as f:
                    json.dump(all_users, f, indent=4)
                print(f"Welcome, {login}\n")
                with open(f"{path}/balance/{login}_balance.txt", "w") as bal:
                    bal.write(str(float(default_money)))
                with open(f"{path}/transactions/{login}_history.json", "w"
                          ) as h:
                    trans = {"id_1": str(default_money)}
                    json.dump(trans, h, indent=4)

                time.sleep(1)
                operations(login)
            else:
                new_user()
    else:
        new_user()


# menu for all avialable operations.
# incasator is redirecting to hiden incasator menu
def operations(login):
    print("OPERATIONS")
    if login == "incasator":
        incasator_menu(login)
    else:
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


# menu with incasator commands
def incasator_menu(login):
    choice = int(input("1. Check ATM\n2. Load ATM\n3. Exit\n"))
    if choice == 1:
        with open(f"{path}/ATM_cash.json") as f:
            cash = json.load(f)
        for k, v in cash.items():
            print(f"{k}: {v} шт.")
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


# loading ATM with avialable nominals
def load_atm(login):
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


# checkin user balance
def balance(login):
    with open(f"{path}/balance/{login}_balance.txt") as f:
        bal = round(float(f.read()), 2)
        print("Your balance is: " + str(bal) + "$")
        time.sleep(2)
        operations(login)


# deposit money to account
def deposit(login):
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
                transactions(login, str(new_bal))
            print("Done")
            time.sleep(1)
            operations(login)
    except ValueError:
        print("Only numbers")
        deposit(login)


# widthraw money from ATM
def withdraw(login):
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
                            transactions(login, str(new_bal))
                        print("Done")
                        time.sleep(1)
                        operations(login)
                    else:
                        withdraw(login)
    except ValueError:
        print("Only numbers")
        withdraw(login)


# cheking if it is possible to withdraw drom ATM
def counter(withdr):
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


def transactions(login, new_bal):
    with open(f"{path}/transactions/{login}_history.json") as f:
        history = json.load(f)
    new_id = len(history)
    history[f"id_{new_id + 1}"] = new_bal
    with open(f"{path}/transactions/{login}_history.json", "w") as f:
        json.dump(history, f, indent=4)


def history(login):
    with open(f"{path}/transactions/{login}_history.json") as f:
        history = json.load(f)
        print("HISTORY")
        for i in history:
            print(f"{i} {history[i]}")
        time.sleep(2)
        operations(login)


if __name__ == "__main__":
    print("WELCOME TO E-BANK\n")
    time.sleep(1)
    if not os.path.exists(f"{path}/transactions/"):
        os.mkdir(f"{path}/transactions")
    if not os.path.exists(f"{path}/balance/"):
        os.mkdir(f"{path}/balance")
    if not os.path.exists(f"{path}/users.json"):
        with open(f"{path}/users.json", "w")as f:
            a = {}
            json.dump(a, f)
        with open(fr"{path}/users.json") as f:
            all_users = json.load(f)
        all_users[incasator_name] = incasator_pass
        with open(fr"{path}/users.json", "w") as f:
            json.dump(all_users, f, indent=4)
    if not os.path.exists(f"{path}/ATM_cash.json"):
        with open(f"{path}/ATM_cash.json", "w") as f:
            json.dump(avialable_nominals, f)
    start()
