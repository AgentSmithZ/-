x = []

for i in range(1, 13):
    length = float(input(f'Вводи длину сторону {i}: '))
    x.append(length)

sum = sum(x)
print(f'{sum}')
