class calc:
    def __init__(self, x):
        self.x = x

    def calculate(self):
        self.x = self.x // 100

    def result(self):
        print(self.x)

obj = calc(2000)
obj.calculate()
obj.result()
