import math

def k(x):
    if math.sin(x) >= 0:
        return x ** 2
    else:
        return abs(x)
    
def f(x):
    k_value = k(x)
    if k_value < x:
        return abs(x)
    else: 
        return k_value * x
    
x = 2
ever = f(x)
print(ever)
