import math

def distance(x, y):
    circle = math.pi * x ** 2
    square = y ** 2
    if circle < square:
        return "Площадь круга больше"
    elif circle > square:
        return "Площадь квадрата больше."
    else:
        return "Площади равны."
    
def main():
    try: 
        x = float(input('Введите радиус круга: '))
        y = float(input('Введите квадрата: '))

        result = distance(x, y)
        print(result)
    except ValueError:
        print("Вводи числа.")

if __name__ == "__main__":
    main()
