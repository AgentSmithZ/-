def distance(x, y):
    ft_to_km = y * 0.0003048
    if x < ft_to_km:
        return "Расстояние в километрах меньше."
    elif x > ft_to_km:
        return "Расстояние в футах меньше."
    else:
        return "Расстояния равны."
    
def main():
    try: 
        x = float(input('Введите расстояние в км: '))
        y = float(input('Введите расстояние в футах: '))

        result = distance(x, y)
        print(result)
    except ValueError:
        print("Вводи числа.")

if __name__ == "__main__":
    main()
