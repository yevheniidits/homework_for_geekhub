""" Створiть 3 рiзних функцiї (на ваш вибiр).
Кожна з цих функцiй повинна повертати якийсь результат.
Також створiть четверу ф-цiю, яка в тiлi викликає 3 попереднi,
обробляє повернутий ними результат та також повертає результат.
Таким чином ми будемо викликати 1 функцiю, а вона в своєму тiлi ще 3 """


def firstName():
    first_name = str(input("Ім'я: "))
    return first_name


def secondName():
    second_name = str(input("Прізвище: "))
    return second_name


def middleName():
    middle_name = str(input("По-батькові: "))
    return middle_name


def fullName():
    print("Вас звати " + firstName() + " " + middleName() + " " + secondName())


fullName()
