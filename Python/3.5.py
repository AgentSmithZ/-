class calc:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def calculate1(self):
        return self.x // self.y

obj = calc(540,130,130)
obj.calculate1()
print(obj.calculate1())
