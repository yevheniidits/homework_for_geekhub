"""
Створити клас Calc, який буде мати атребут last_result та 4 методи.
Методи повинні виконувати математичні операції з 2-ма числами,
а саме додавання, віднімання, множення, ділення.
- Якщо під час створення екземпляру класу звернутися до атребута last_result
він повинен повернути пусте значення
- Якщо використати один з методів - last_result повенен повернути результат
виконання попереднього методу.
- Додати документування в клас (можете почитати цю статтю:
https://realpython.com/documenting-python-code/ )
"""


class Calc(object):
    """
    A class to make simple arithmetic operations

    ...

    Attributes
    ----------
    last_result :
        remember result of previous used method,
        can be used as argument in methods

    Methods
    -------
    plus (x: float, y: float)
        last_result = x + y and return last_result

    minus (x: float, y: float)
        last_result = x - y and return last_result

    multiply (x: float, y: float)
        last_result = x * y and return last_result

    divide (x: float, y: float)
        if try to divide by zero (y = 0) print error message,
        else last_result = x / y and return last_result
    """

    last_result = None

    def plus(self, x, y):
        """ takes two arguments, return x + y """
        self.last_result = x + y
        return self.last_result

    def minus(self, x, y):
        """ takes two arguments, return x - y """
        self.last_result = x - y
        return self.last_result

    def multiply(self, x, y):
        """ takes two arguments, return x * y """
        self.last_result = x * y
        return self.last_result

    def divide(self, x, y):
        """ takes two arguments, return x / y """
        if y == 0:
            return "Division by zero"
        else:
            self.last_result = x / y
            return self.last_result


# test
res = Calc()
print(res.last_result)
print(res.plus(4, 5))
print(res.last_result)
print(res.minus(res.last_result, 19))
print(res.last_result)
