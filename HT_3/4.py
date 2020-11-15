""" Написати функцію < prime_list >, яка прийматиме 2 аргументи -
початок і кінець діапазона, і вертатиме список простих чисел
всередині цього діапазона.
"""


def prime_list(start, stop):
    if start > stop:
        print("Кінець діапазону не може бути меньший, ніж початок")
        exit()
    if stop < 2:
        print("Немає простих чисел в заданому діапазоні")
        exit()
    if start < 2:
        start = 2
    for i in range(start, stop + 1):
        is_prime = True
        for j in range(2, i):
            if not i % j:
                is_prime = False
        if is_prime:
            print(i)


a = int(input("Від: "))
b = int(input("До: "))
prime_list(a, b)
