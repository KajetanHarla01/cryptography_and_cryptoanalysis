from sympy import *
def factorial(n):
    if n == 0:
        return 1
    else:
        return n*factorial(n-1)

def generate_pascal_triangle(n):
    triangle = []
    for i in range(n):
        row = [1] * (i + 1)
        for j in range(1, i):
            row[j] = triangle[i - 1][j - 1] + triangle[i - 1][j]
        triangle.append(row)
    return triangle   


option = int(input("Check option number (1 - 6): "))

if option == 1:
    print("1) Find the sum of the terms of a geometric series.")
    a = float(input("a = "))
    q = float(input("q = "))
    if abs(q) < 1 or a == 0:
        sum = a / (1 - q)
        print("The geometric series is always convergent.")
        print("S = " + str(sum))
    else:
        print("The geometric series is divergent.")
        print("S = inf")
elif option == 2:
    print("2) Evaluate n!.")
    n = int(input("n = "))
    print(str(n) + "! = " + str(factorial(n)))
elif option == 3:
    print("3) Evaluate binomial coefficients.")
    n = int(input("n = "))
    k = int(input("k = "))
    res = factorial(n) / (factorial(k) * factorial(n - k))
    print("Result = " + str(res))
elif option == 4:
    print("4) Print out Pascal's triangle.")
    layers = int(input("n = "))
    pascal_triangle = generate_pascal_triangle(layers)
    for row in pascal_triangle:
        print(row)
elif option == 5:
    print("5) Use the sieve of Eratosthenes to find all primes less than 10000.")
    n = 10000
    is_prime = [True] * n
    is_prime[0] = is_prime[1] = False

    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, n, i):
                is_prime[j] = False

    primes = [i for i in range(n) if is_prime[i]]
    print(primes)
elif option == 6:
    print("6) Verify Goldbach’s conjecture for all even integers less than 10000.")
    n = 10000
    for i in range(4, n, 2):
        firstNum = prevprime(i)
        secNum = i - firstNum
        while not isprime(secNum):
            firstNum = prevprime(firstNum)
            secNum = i - firstNum
        print(f"{i} = {firstNum} + {secNum}")
else:
    print("Incorrect option number.")