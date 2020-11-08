""" Write a script to remove duplicates from Dictionary """

d = {'a': 100, 'b': 200, 'c': 300, 'd': 300}
result = {}

for key, value in d.items():
    if value not in result.values():
        result[key] = value

print(result)
