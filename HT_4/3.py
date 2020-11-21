""" На основі попередньої функції створити наступний кусок кода:
   а) створити список із парами ім'я/пароль різноманітних видів
   (орієнтуйтесь по правилам своєї функції) - як валідні, так і ні;
   б) створити цикл, який пройдеться по цьому циклу і, користуючись
   валідатором, перевірить ці дані і надрукує для кожної пари значень
   відповідне повідомлення, наприклад:
      Name: vasya
      Password: wasd
      Status: password must have at least one digit
      -----
      Name: vasya
      Password: vasyapupkin2000
      Status: OK
   P.S. Не забудьте використати блок try/except ;)
"""


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


def validator(login, password):
    status = "OK"
    try:
        if len(login) < 3 or len(login) > 50:
            raise lenError(len(login), "Login")
        else:
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

    except lenError as err1:
        status = ("{} length must be {} characters"
                  .format(err1.field, err1.length))
    except difficultError as err2:
        status = ("Password must have at least 1 {}".format(err2.value))

    return status


users = [{"In": "Qwerty1q"}, {"Adam": "power3000"},
         {"Stepan": "123zZc123"}, {"admin": "admin"},
         {"TurboAnna": "trololo"}]

for i in users:
    for key, value in i.items():
        print("Name: " + str(*i.keys()))
        print("Password: " + str(*i.values()))
        print("Status: " + validator(key, value))
