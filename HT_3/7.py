""" Написати функцію, яка приймає на вхід список
і підраховує кількість однакових елементів у ньому.
"""


def analys(some_list):
    temp_dict = {}
    for i in some_list:
        if i in temp_dict:
            temp_dict[i] += 1
        else:
            temp_dict[i] = 1
    for item in sorted(temp_dict):
        print("{}: {}".format(item, temp_dict[item]))


n = input("Введіть елементи спику через пробіл: ").split()
user_list = list(n)
analys(user_list)
