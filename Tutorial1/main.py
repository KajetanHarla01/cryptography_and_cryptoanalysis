def factorial(n):
    if n == 0:
        return 1
    else:
        return n*factorial(n-1)

def pascal_triangle(n, tab = []):
    if len(tab) == n:
        return
    temp = []
    temp.append(1)
    for i in range(0, len(tab) - 1):
        temp.append(tab[i] + tab[i+1])
    for element in temp:
        print(str(element) + " ")
    #print("\n")
    print(len(temp))
    return pascal_triangle(n, temp)    


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
    pascal_triangle(layers)
else:
    print("Incorrect option number.")