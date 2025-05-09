n = float(input('Вводи натуральные числа n: '))

if n <= 0:
    print("n должно быть натуральным числом")
else: 
    x = []

for i in range (1, 11):
    numbers = float(input(f'Вводи вещественные числа a{i}: '))
    x.append(numbers)

sum = sum(x)
print(f'{sum}')
