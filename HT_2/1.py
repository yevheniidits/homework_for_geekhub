""" Створити цикл від 0 до ... (вводиться користувачем).
В циклі створити умову, яка буде виводити поточне значення,
якщо остача від ділення на 17 дорівнює 0. """

a = int(input("Введіть число: "))
for i in range(a):
    if i % 17 == 0:
        print(i)
