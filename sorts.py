from random import randint
import time

N = 1000
a = []

for i in range(N):
    a.append(randint(1, 9999))

print(a)


def bubble_sort(my_list):
    print('bubble sort')
    for i in range(len(my_list) - 1):
        for j in range(len(my_list) - i - 1):
            if my_list[j] > my_list[j + 1]:
                my_list[j], my_list[j + 1] = my_list[j + 1], my_list[j]
            j += 1
        i += 1


def select_sort(my_list):
    print('select_sort')
    for i in range(len(my_list) - 1):
        temp = i
        j = i + 1
        while j < len(my_list):
            if my_list[j] < my_list[temp]:
                temp = j
            j += 1
        my_list[i], my_list[temp] = my_list[temp], my_list[i]


bubble = a

start_time = time.time()
bubble_sort(bubble)
print(bubble)
print(time.time() - start_time)

select = a

start_time = time.time()
select_sort(select)
print(select)
print(time.time() - start_time)
