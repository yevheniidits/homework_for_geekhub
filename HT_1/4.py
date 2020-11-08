""" Write a script to concatenate N strings """

N = int(input('Number of strings: '))
conc_str = str()
for i in range(N):
    temp_str = str(input('Enter ' + str(i + 1) + ' string: '))
    conc_str = str(conc_str) + str(temp_str)
print(conc_str)
