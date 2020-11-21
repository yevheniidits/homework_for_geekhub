""" Всі ви знаєте таку функцію як <range>.
Напишіть свою реалізацію цієї функції.
   P.S. Повинен вертатись генератор.
   P.P.S. Для повного розуміння цієї функції - можна почитати
   документацію по ній: https://docs.python.org/3/library/stdtypes.html#range
"""


class rangeError(Exception):
    pass


def custom_range(start: int, stop=0, step=1):
    if stop == 0:
        stop = start
        start = 0
    if start > stop and step > 0:
        raise rangeError()
    elif start < stop and step < 0:
        raise rangeError()
    else:
        while start != stop:
            yield start
            start += step


print(list(custom_range(2, 20)))
