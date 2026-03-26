import math

def triangle_type(a, b, c):
    if a == b == c:
        return "равносторонний"
    elif a == b or b == c or a == c:
        return "равнобедренный"
    else:
        return "разносторонний"

def triangle_area(a, b, c):
    s = (a + b + c) / 2 
    area = math.sqrt(s * (s - a) * (s - b) * (s - c))
    return area

def main():
    try:
        a = float(input("Введите сторону треугольника a: "))
        b = float(input("Введите сторону треугольника b: "))
        c = float(input("Введите сторону треугольника c: "))

        ttype = triangle_type(a, b, c)
        tarea = triangle_area(a, b, c)
        print(f"Треугольник является: {ttype}.")
        print(f"Площадь треугольника: {tarea}.")

    except ValueError:
        print("Ошибочка")

if __name__ == "__main__":
    main()
