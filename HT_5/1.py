""" Програма-банкомат.
   Створити програму з наступним функціоналом:
      - підтримка 3-4 користувачів, які валідуються парою ім'я/пароль
      (файл <users.data>);
      - кожен з користувачів має свій поточний баланс
      (файл <{username}_balance.data>) та історію транзакцій
      (файл <{username}_transactions.data>);
      - є можливість як вносити гроші, так і знімати їх.
      Обов'язкова перевірка введених даних (введено число;
      знімається не більше, ніж є на рахунку).
   Особливості реалізації:
      - файл з балансом - оновлюється кожен раз при зміні балансу
      (містить просто цифру з балансом);
      - файл - транзакціями - кожна транзакція у вигляді JSON рядка
      додається в кінець файла;
      - файл з користувачами: тільки читається. Якщо захочете
      реалізувати функціонал додавання нового користувача -
      не стримуйте себе :)
   Особливості функціонала:
      - за кожен функціонал відповідає окрема функція;
      - основна функція - <start()> - буде в собі містити весь
      workflow банкомата:
      - спочатку - логін користувача - програма запитує ім'я/пароль.
      Якщо вони неправильні - вивести повідомлення про це і закінчити
      роботу (хочете - зробіть 3 спроби, а потім вже закінчити роботу -
      все на ентузіазмі :) )
      - потім - елементарне меню типа:
        Введіть дію:
           1. Продивитись баланс
           2. Поповнити баланс
           3. Вихід
      - далі - фантазія і креатив :)
 """


import json
import os
import time


path = fr'{os.path.dirname(__file__)}'

# set start deposit
default_money = 1000


def start():
    # main menu
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
        print("Wrong option! Try again\n")
        start()


def log_in():
    # login/password validation
    with open(fr"{path}/users.json") as f:
        all_users = json.load(f)
    login = input("Login: ")
    if login in all_users:
        check_pass = all_users[login]
        # you can change number of attemps to input password
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


def new_user():
    with open(fr"{path}/users.json") as f:
        all_users = json.load(f)
    # check if user already exists
    login = input("CREATE NEW ACCOUNT\nLogin: ")
    if login in all_users:
        print("This user already exists")
        time.sleep(2)
        start()
    else:
        # create new user
        password = input("Password: ")
        new_pass = {"password": password}
        all_users[login] = new_pass

        with open(fr"{path}/users.json", "w") as f:
            json.dump(all_users, f, indent=4)
        print(f"Welcome, {login}\n")
        # set balance to <default_money>
        with open(f"{path}/balance/{login}_balance.txt", "w") as bal:
            bal.write(str(float(default_money)))
        # add line to history with default balance
        with open(f"{path}/transactions/{login}_history.json", "w") as h:
            trans = {"id_1": str(default_money)}
            json.dump(trans, h, indent=4)

        time.sleep(1)
        operations(login)


def operations(login):
    print("OPERATIONS")
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


def balance(login):
    with open(f"{path}/balance/{login}_balance.txt") as f:
        bal = round(float(f.read()), 2)
        print("Your balance is: " + str(bal) + "$")
        time.sleep(2)
        operations(login)


def deposit(login):
    # chek for valid input (only numbers > 0)
    try:
        depo = input("Amount: ")
        if float(depo) <= 0:
            print("More than 0")
            time.sleep(1)
            deposit(login)
        else:
            # write new deposit to balance and balance history
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


def withdraw(login):
    try:
        depo = input("Amount: ")
        if float(depo) <= 0:
            print("More than 0")
            time.sleep(1)
            withdraw(login)
        else:
            with open(f"{path}/balance/{login}_balance.txt") as f:
                # check if user have enough money
                new_bal = float(f.read()) - float(depo)
                if new_bal < 0:
                    print("Not enough money")
                    withdraw(login)
                else:
                    # write new deposit to balance and balance history
                    with open(f"{path}/balance/{login}_balance.txt", "w") as f:
                        f.write(str(new_bal))
                        transactions(login, str(new_bal))
                    print("Done")
                    time.sleep(1)
                    operations(login)
    except ValueError:
        print("Only numbers")
        deposit(login)


def transactions(login, new_bal):
    # add new line after deposit/withdraw to history with new id
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
    start()
