class calc:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def calculate1(self, n):
        if n < 1 or n > self.x * self.y:
            raise ValueError("Номер вне диапазона")
        return (n - 1) // self.y + 1
    
    def calculate2(self, n):
        if n < 1 or n > self.x * self.y:
            raise ValueError("Номер вне диапазона")
        return (n - 1) % self.y + 1

obj = calc(10,5)
n = 23
x_first = obj.calculate1(n)
x_second = obj.calculate2(n)

print(f'Значение: {n} находится в строке {x_first} и столбце {x_second}')
