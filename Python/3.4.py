class calc:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def calculate1(self):
        return self.x // self.y
    
    def calculate2(self):
        return self.x % self.y

obj = calc(10,5)
obj.calculate1()
obj.calculate2()
print('Досталось: ', obj.calculate1(), '| Остаток: ', obj.calculate2())
