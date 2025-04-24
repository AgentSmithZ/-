class calc:

    def __init__(self, x):
        self.x = x
    
    def calculate(self):
        ever = str(self.x)
        return int(ever[:-2] + ever[2] + ever[1])

calculator = calc(721)

print(calculator.calculate())
