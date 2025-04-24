class calc:
    def __init__(self, x):
        self.x = x

    def calculate(self):
        ever = str(self.x)
        return int(ever[-1] + ever[:-1])
    
calculator = calc(275)

print(calculator.calculate())
