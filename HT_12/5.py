"""
Створити пустий клас, який називається Thing. Потім створіть об'єкт example
цього класу. Виведіть типи зазначених об'єктів.
"""


class Thing(object):
    pass


example = Thing()
example_2 = Thing()
print(type(example))        # <class '__main__.Thing'>
print(type(example_2))      # <class '__main__.Thing'>
