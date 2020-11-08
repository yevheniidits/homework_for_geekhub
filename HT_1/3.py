""" Write a script to sum of the first n positive integers. """

n = int(input("Input a number: "))
summa = 0
for i in range(n + 1):
    summa += i
print(summa)
