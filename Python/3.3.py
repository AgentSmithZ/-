class calc:
    def __init__(self, x):
        self.x = x

    def calculate(self):
        self.x = self.x // 7

    def result(self):
        print(self.x)

obj = calc(234)
obj.calculate()
obj.result()
