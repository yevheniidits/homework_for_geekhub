"""
Створіть клас в якому буде атребут який буде рахувати кількість створених
екземплярів класів.
"""


class MyClass(object):
    count = 0

    def __init__(self):
        self.__class__.count += 1
        print(f'{self.count} initialization')

    def counter(self):
        print(f'Total: {self.count} initialization(s)')


# test
a = MyClass()
b = MyClass()
b.counter()
c = MyClass()
a.counter()
