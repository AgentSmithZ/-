import math

class calc:
    def __init__(self, x):
        self.x = x

    def calculate(self):
        if self.x > 0:
            ever = pow(math.sin(self.x), 2) * self.x
        else:
            ever = 1 - 2 * math.sin(self.x) * pow(self.x, 2)
        return ever
    
obj = calc(15)
obj.calculate()
print(obj.calculate())
