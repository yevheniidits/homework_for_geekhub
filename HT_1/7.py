""" Write a script to concatenate all elements in a list
    into a string and print it"""


def concatenate_list_data(list):
    result = ''
    for element in list:
        result += str(element)
    return result


print(concatenate_list_data([4, 3, 5, 3, 9, 23]))
