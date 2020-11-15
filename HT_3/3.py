""" Написати функцию < is_prime >, яка прийматиме 1 аргумент -
число від 0 до 1000, и яка вертатиме True, якщо це число просте,
и False - якщо ні.
"""


def is_prime(x):
    # перевіряємо вихід за межі завдання
    if x < 0 or x > 1000:
        x = int(input("Введіть число від 0 до 1000: "))
        is_prime(x)
    elif x < 2:
        return False
    for i in range(2, x):
        if not x % i:
            return False
    return True


num = int(input("Введіть число від 0 до 1000: "))
print(is_prime(num))
