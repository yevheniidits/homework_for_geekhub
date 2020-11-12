""" Маємо рядок -->
"f98neroi4nr0c3n30irn03ien3c0rfekdno400wenwkowe00ko
ijn35pijnp46ij7k5j78p3kj546p465jnpoj35po6j345" -> просто потицяв по клавi
   Створіть ф-цiю, яка буде отримувати рядки на зразок цього,
   яка оброблює наступні випадки:
-  якщо довжина рядка в діапазонi 30-50 ->
   прiнтує довжину, кiлькiсть букв та цифр
-  якщо довжина менше 30 ->
   прiнтує суму всiх чисел та окремо рядок без цифр (лише з буквами)
-  якщо довжина бульше 50 - > ваша фантазiя
"""


def someFunc(user_input):
    l = len(user_input)
    num = ''
    lett = ''
    summa = 0

    for char in user_input:
        if char.isdigit():
            num += char  # only digits
            summa += int(char)  # sum of all digits
        if char.isalpha():
            lett += char  # only letters

    if 30 <= l <= 50:
        print("Довжина рядка: " + str(l) + " Букв: " +
              str(len(lett)) + " Цифр: " +
              str(len(num)))
    elif l < 30:
        print("Сумма чисел: " + str(summa) + " Лише цифри: " + str(num))
    else:
        print("Не ламай клавіатуру!!!")


user_input = input("Потицяйте по клаві: ")
someFunc(user_input)
