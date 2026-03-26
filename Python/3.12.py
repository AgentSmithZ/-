class calc:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def calculate1(self, ever):
        return(ever - 1) // self.y + 1
    
    def calculate2(self, ever1):
        return(ever1 - 1) % self.y + 1

obj = calc(5,4)
ever1 = 15
x_first = obj.calculate1(ever1)
x_second = obj.calculate2(ever1)

print(f'Квартира: {ever1} находится на {x_first} этаже и по счёту {x_second}-й на этаже')
