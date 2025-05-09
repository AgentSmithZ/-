class calc:
    def __init__(self, x):
        self.x = x
    
    def calculate(self):
        ever = str(self.x)
        print(ever)
        everone = ever[:-2] + ever[2] + ever[1]
        print(everone)
        evertwo = ever[1] + ever[0]+ever[2:]
        print(evertwo)
        everthree = ever[1] + ever[2:] + ever[0]
        print(everthree)
        everfour = ever[2:] + ever[1] + ever[0]
        print(everfour)
        everfive = ever[2:] + ever[0] + ever[1]
        print(everfive)

obj = calc(782)
obj.calculate()
