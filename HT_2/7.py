""" Ну і традиційно -> калькулятор :) повинна бути 1 ф-цiя
яка б приймала 3 аргументи - один з яких операцiя, яку зробити! """


def calc(x, operation, y):
    if operation == "+":
        return x + y
    elif operation == "-":
        return x - y
    elif operation == "*":
        return x * y
    elif operation == "/":
        try:
            return x / y
        except ZeroDivisionError:
            print("Не можна ділити на 0")


x = int(input("Введіть x: "))
operation = input("Введіть операцію (+, -, *, /): ")
y = int(input("Введіть y: "))
print("Результат: " + str(calc(x, operation, y)))
