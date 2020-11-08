""" Write a script to replace last value of tuples in a list."""

replace_element = int(input('Enter element: '))
test_list = [(10, 20, 40), (40, 50, 60), (70, 80, 90)]
print([t[:-1] + (replace_element,) for t in test_list])
