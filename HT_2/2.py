""" Користувачем вводиться початковий і кінцевий рік.
Створити цикл, який виведе всі високосні роки
в цьому проміжку (границі включно). """

year_start, year_end = map(int, input(
    "Введіть початковий і кінцевий роки через пробіл: ").split())
for year in range(year_start, year_end + 1):
    if year % 400 == 0 or year % 4 == 0 and year % 100 != 0:
        print(year)
