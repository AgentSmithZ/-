class calc:
    def __init__(self, x):
        self.x = x
    
    def calculate(self):
        ever = str(self.x)
        return ever[1] + ever[0] + ever[2:]

obj = calc(613)
obj.calculate()
print(obj.calculate())
