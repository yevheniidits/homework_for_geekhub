""" Створіть функцію, всередині якої будуть записано список із п'яти
користувачів (ім'я та пароль).
Функція повинна приймати три аргументи: два - обов'язкових (<username>
та <password>) і третій - необов'язковий параметр <silent> (значення за
замовчуванням - <False>).
Логіка наступна:
    якщо введено коректну пару ім'я/пароль - вертається <True>;
    якщо введено неправильну пару ім'я/пароль і <silent> == <True> -
    функція вертає <False>, інакше (<silent> == <False>) -
    породжується виключення LoginException
"""


class LoginException(Exception):
    pass


def login_validator(username, password, silent=False):
    users = [{"Ivan": "qwerty1"}, {"Adam": "power3000"},
             {"Stepan": "123zxc123"}, {"admin": "admin"},
             {"TurboAnna": "trololo"}]
    passwords = []
    user = []
    for dic in users:
        user.extend(dic.keys())
        passwords.extend(dic.values())
    if username in user:
        if password == passwords[user.index(username)]:
            return True
        else:
            if silent:
                return False
            else:
                raise LoginException()
    else:
        if silent:
            return False
        else:
            raise LoginException()


username = input("Login: ")
password = input("Password: ")
print(login_validator(username, password, silent=True))
