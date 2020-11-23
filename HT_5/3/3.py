""" Написати функцію, яка приймає два параметри:
ім'я файлу такількість символів.
   На екран повинен вивестись список із трьома блоками -
   символи з початку, із середини та з кінця файлу.
   Кількість символів в блоках - та, яка введена в другому параметрі.
   Придумайте самі, як обробляти помилку, наприклад,
   коли кількість символів більша, ніж є в файлі
   (наприклад, файл із двох символів і треба вивести по
   одному символу, то що виводити на місці середнього блоку символів?)
"""


import os.path


def strange_func(file, number):
    if not os.path.isfile(file):
        print("File not found")
        return

    elif number <= 0:
        print("Incorrect number of symbols")
        return

    with open(file) as f:
        length = len(f.read())
        if length < number:
            print("Not enough symbols in file")
            return
        else:
            f.seek(0)
            print(f"First: {f.read(number)}")

            if (length - number) % 2 == 0:
                f.seek((length - number) / 2)
                print(f"Middle: {f.read(number)}")
            else:
                # if length of file is odd we will print 1 more symbol
                f.seek((length - number) / 2)
                print(f"Middle: {f.read(number + 1)}")

            f.seek(length - number)
            print(f"Last: {f.read()}")


strange_func('test_text.txt', 3)
