x = []

inp = int(input('Вводи кол-во человек:'))

for i in range(inp):
    salary = float(input(f'Вводи зарплату человека {i+1}: '))
    x.append(salary)

sum = sum(x)
print(f'{sum}')
