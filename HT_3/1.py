""" Написати функцію < square > , яка прийматиме один аргумент -
сторону квадрата, і вертатиме 3 значення (кортеж): периметр квадрата,
площа квадрата та його діагональ.
"""


def square(x):
    return (4 * x, x ** 2, (2 * x ** 2) ** 0.5)


length = float(input("Сторона квадрата: "))
print(square(length))
