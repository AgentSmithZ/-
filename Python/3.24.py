class calc:

    def __init__(self, x):
        self.x = x
    
    def calculate(self):
        ever = str(self.x)
        return int(ever[1] + ever[0] + ever[2:])

calculator = calc(721)

print(calculator.calculate())
