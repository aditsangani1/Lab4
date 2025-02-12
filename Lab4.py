def fibonacci(num):
    if num == 1:
        return 0
    num1 = 0
    num2 = 1
    for number in range(1, num + 1):
        num3 = num1 + num2
        num2 = num1
        num1 = num3
    return num3

print(fibonacci(3))

