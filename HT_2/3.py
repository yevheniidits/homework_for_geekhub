""" Написати функцiю season, яка приймає один аргумент — номер мiсяця
(вiд 1 до 12), яка буде повертати пору року,
якiй цей мiсяць належить (зима, весна, лiто або осiнь) """


def season(month):
    if 3 <= month <= 5:
        return "Весна"
    elif 6 <= month <= 8:
        return "Літо"
    elif 9 <= month <= 11:
        return "Осінь"
    else:
        return "Зима"


a = int(input("Номер місяця від 1 до 12: "))
print(season(a))
