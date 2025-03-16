a = int(input("Введите a -> "))
print(a)
b = int(input("Введите b -> "))
print(b)

while( a != b):
    if (a > b):
        a=a-b
    else:
        b=b-a
print(a, b)
file = open("res.txt", "w")
file.write( str(a) + "      " +str(b))
file.close()