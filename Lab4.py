def fibonacci(num):
    if num == 1:
        return 0
    num1 = 0
    num2 = 1
    for number in range(1, num):
        num3 = num1 + num2
        num2 = num1
        num1 = num3
    return num3

def is_prime(num):
    if num <= 1:
        return False
    for i in range(2, num):
        if num % i == 0:
            return False
    return True

def print_prime_factors(num):
    pass











