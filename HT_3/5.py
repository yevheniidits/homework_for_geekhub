""" Написати функцію < fibonacci >, яка приймає один аргумент
і виводить всі числа Фібоначчі, що не перевищують його.
"""


def fibonacci(n):
    if n <= 0:
        n = float(input("Введіть число, більше 0: "))
        fibonacci(n)
    else:
        fib1 = 0  # для послідовності від 1 змінити fib1 = 1
        fib2 = 1
        print(fib1)
        while fib2 <= n:
            fib1, fib2 = fib2, fib1 + fib2
            print(fib1)


n = float(input("Введіть число, більше 0: "))
fibonacci(n)
