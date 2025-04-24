import math

class calc:
    def __init__(self, y):
        self.y = y

    def calculate(self):
        if self.y > 3:
            return 'Точка попадает в область II'
        elif self.y == 3:
            return 'Введите другое число'
        else:
            return 'Точка попадает в область I'
    
    
obj = calc(15)
obj.calculate()
print(obj.calculate())
