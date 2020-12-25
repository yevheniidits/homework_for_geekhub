"""
Створити клас Person, в якому буде присутнім метод __init__ який буде
приймати * аргументів, які зберігатиме в відповідні змінні.
Методи, які повинні бути в класі Person -
show_age, print_name, show_all_information.
- Створіть 2 екземпляри класу Person та в кожному з екземплярів створіть
атребут profession.
"""


class Person(object):
    """
    Create information about Person

    ...

    Methods
    -------
    __init__ :
        contains basic information like name, surname, age etc.

    show_age
        print persons age

    print_name
        print persons name and surname

    show_all_information
        print all information about person in format "key: value"

    """

    def __init__(self, name, surname, age):
        self.name = name
        self.surname = surname
        self.age = age

    @property
    def show_age(self):
        print(self.age)

    @property
    def print_name(self):
        print(' '.join([self.name, self.surname]))

    @property
    def show_all_information(self):
        for key, value in self.__dict__.items():
            print(': '.join([str(key), str(value)]))


# test
pers1 = Person('Ivan', 'Popov', 40)
pers2 = Person('Petro', 'Sobolev', 50)
pers1.profession = 'driver'
pers2.profession = 'teacher'

pers1.print_name
pers2.show_age

pers1.show_all_information
pers2.show_all_information
