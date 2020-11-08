""" Write a script to convert decimal to hexadecimal """

dec_number = int(input('Input decimal numbers: '))
print(hex(dec_number).split('x')[-1])
