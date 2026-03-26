def calculate1(x):
    if x <= 2:
        return 2
    else:
        return 2 + 2(x - 2)
        
def calculate2(x):
    if x < 0:
        return 3 + x
    else:
        return 3 - x

x_first = 2
x_second = 1

y_first = calculate1(x_first)
y_second = calculate2(x_second)

print(f'График (a) при X = {x_first}: Y = {y_first}')
print(f'График (b) при X = {x_second}: Y = {y_second}')
