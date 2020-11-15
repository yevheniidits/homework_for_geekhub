""" Вводиться число. Якщо це число додатне, знайти його квадрат,
якщо від'ємне, збільшити його на 100, якщо дорівнює 0, не змінювати.
"""


def my_func(num):
    if num == 0:
        return num
    elif num > 0:
        return num ** 2
    else:
        return num + 100


n = float(input("Введіть число: "))
print(my_func(n))
