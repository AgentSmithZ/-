import math

class calc:
    def __init__(self, x):
        self.x = x

    def calculate(self):
        if self.x > 4:
            return 'Точка попадает в область I'
        elif self.x == 4:
            return 'Введите другое число'
        else:
            return 'Точка попадает в область II'
    
    
obj = calc(15)
obj.calculate()
print(obj.calculate())
