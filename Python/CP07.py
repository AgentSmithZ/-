def max_consecutive_digits(s):
    current_count = 0 
    max_count = 0  

    for char in s:
        if char.isdigit():
            current_count += 1
        else:
            max_count = max(max_count, current_count)
            current_count = 0  
    
    return max(max_count, current_count)

alfabit = 'abc85182defg86fdftimdk391'
print("Максимальная длина последовательности цифр:", max_consecutive_digits(alfabit))
