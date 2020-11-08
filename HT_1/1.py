""" Write a script which accepts a sequence of comma-separated numbers
from user and generate a list and a tuple with those numbers """


user_data = input("Input some comma-seprated numbers: ")
list = user_data.split(", ")
tuple = tuple(list)
print('List: ', list)
print('Tuple: ', tuple)

