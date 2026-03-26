class calc:
    def __init__(self, x):
        self.x = x

    def calculate1(self):
        return len(self.x) == 3 and self.x.isdigit()
    
    def calculate2(self):
        if self.calculate1():
            return ', '.join(self.x)
        else:
            raise ValueError("Введите трёхзначное число")
        
def main():
    inp = input("Введите трёхзначное число: ")
    ever = calc(inp)

    try:
        ever1 = ever.calculate2()
        print(ever1)
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()
