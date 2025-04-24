class calc:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def calculate1(self):
        inp = int(input('Номер места: '))
        if inp > self.x * self.y:
            print('Нет такого места')
        elif inp % self.y == 0:
            ever = inp // self.y
        else:
            ever = inp // self.y + 1
            print(ever)

obj = calc(9,4)
obj.calculate1()
