def distance(x, y):
    kmh_to_ms = x / 3.6
    if x < kmh_to_ms:
        return "Скорость в м/с больше."
    elif x > kmh_to_ms:
        return "Скорость в км/ч больше."
    else:
        return "Скорости равны."
    
def main():
    try: 
        x = float(input('Введите скорость в км/ч: '))
        y = float(input('Введите скорость в м/c: '))

        result = distance(x, y)
        print(result)
    except ValueError:
        print("Вводи числа.")

if __name__ == "__main__":
    main()
