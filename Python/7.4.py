x = []

inp = int(input('Вводи кол-во предметов:'))

for i in range(inp):
    mass = float(input(f'Вводи массу предмета {i+1}: '))
    x.append(mass)

sum = sum(x)
print(f'{sum}')
