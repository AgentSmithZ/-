def calculate(x, y):
    if y == 0:
        raise ValueError("Обьём должен быть больше нуля.")
    return x / y

def distance(x, x1, y, y1):
    masses = calculate(x, y)
    masses1 = calculate(x1, y1)

    if masses > masses1:
        return "Первый имеет больше плотность."
    elif masses > masses1:
        return "Второй имеет больше плотность."
    else:
        return "Плотности равны."
    
def main():
    try: 
        x = float(input('Введи массу первого тела (кг): '))
        y = float(input('Введи объём первого тела (м3):'))
        x1 = float(input('Введи массу второго тела (кг): '))
        y1 = float(input('Введи объём второго тела (м3): '))

        result = distance(x, y, x1, y1)
        print(result)
    except ValueError:
        print("Вводи числа.")

if __name__ == "__main__":
    main()
