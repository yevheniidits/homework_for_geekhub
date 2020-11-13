""" Написати функцiю season, яка приймає один аргумент — номер мiсяця
(вiд 1 до 12), яка буде повертати пору року,
якiй цей мiсяць належить (зима, весна, лiто або осiнь) """


def season(month):
    if month < 1 or month > 12:
        print("Ти з якої планети? На Землі 12 місяців.")
        a = int(input("Номер місяця від 1 до 12: "))
        season(a)
    elif 3 <= month <= 5:
        print("Весна")
    elif 6 <= month <= 8:
        print("Літо")
    elif 9 <= month <= 11:
        print("Осінь")
    else:
        print("Зима")


a = int(input("Номер місяця від 1 до 12: "))
season(a)
