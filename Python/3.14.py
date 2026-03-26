class calc:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def calculate1(self, n):
        ever = self.x * self.z
        return (n - 1) // ever + 1
    
    def calculate2(self, n):
        ever = self.x * self.z
        h = 4
        h = (h - 1) // ever
        g = n - h * ever
        return(g - 1) // self.z + 1
    
    def calculate3(self, n):
        ever = self.x * self.z
        h = (n - 1) // ever
        g = n - h * ever
        f = (g - 1) // self.z
        return g - f * self.z
        

obj = calc(9,4,6)
n = 50
x_first = obj.calculate1(n)
x_second = obj.calculate2(n)
x_third = obj.calculate3(n)

print(f'Номер: {n} находится в подьезде {x_first} на этаже {x_second} и является {x_third}-й квартирой на этаже')
