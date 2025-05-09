x = []

for i in range (1, 11):
    numbers = float(input(f'Вводи числа {i}: '))
    x.append(numbers)

sum = sum(x)
print(f'{sum}')
