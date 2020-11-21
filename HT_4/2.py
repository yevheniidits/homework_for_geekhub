""" Створіть функцію для валідації пари ім'я/пароль за наступними правилами:
   - ім'я повинно бути не меншим за 3 символа і не більшим за 50;
   - пароль повинен бути не меншим за 8 символів і повинен мати хоча б одну
   цифру;
   - щось своє :)
   Якщо якийсь із параментів не відповідає вимогам - породити виключення
   із відповідним текстом.
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


def validator():
    try:
        login = input("Login: ")
        if len(login) < 3 or len(login) > 50:
            raise lenError(len(login), "Login")
        else:
            password = input("Password: ")
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
                    print("Hello {}!".format(login))

    except lenError as err1:
        print("{} length must be {} characters"
              .format(err1.field, err1.length))
    except difficultError as err2:
        print("Password must have at least 1 {}".format(err2.value))


validator()
