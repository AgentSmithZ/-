def calculate(x, y):
    if y == 0:
        raise ValueError("Деление не может быть на 0")
    return x / y

def distance(x, x1, y, y1):
    i1 = calculate(x, y)
    i2 = calculate(x1, y1)

    if i1 < i2:
        return "Первый участок имеет меньший ток."
    elif i1 > i2:
        return "Второй участок имеет меньший ток."
    else:
        return "Ток по обоим участкам равны."
    
x = float(input('Введи напряжение на первом участке (U1): '))
y = float(input('Введи сопротивление первого участка (R1): '))
x1 = float(input('Введи напряжение на втором участке (U2): '))
y1 = float(input('Введи сопротивление второго участка (R2): '))

result = distance(x, y, x1, y1)
print(result)
