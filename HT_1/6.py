""" Write a script to check whether a scpecified value
    is conteined in group of values """

test_data = input('Enter test data: ').split()
check_data = input('Check data: ')
if check_data in test_data:
    print('True')
else:
    print('False')
