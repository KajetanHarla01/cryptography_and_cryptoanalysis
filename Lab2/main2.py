import random
import sympy

def format_result(res):
    return "{:.2f}".format(res)

print("----------------------------------")
print("Parameters setting")
s = int(input("Input secret - s: "))
n = int(input("Input shares count - n: "))
t = int(input("Input required shares count - t: "))
sn = []
a = []
a.append(s)

p = int(input("Input prime number - P (or 0 to generate it randomly): "))

if p == 0:
    min_p = (s if s > n else n)  + 1
    prime_num = random.randint(0, 20)
    p = sympy.nextprime(min_p)
    for i in range(prime_num):
        p = sympy.nextprime(min_p)
        min_p = p

for i in range(t - 1):
    a.append(random.randint(1, 1000))

print("P = " + str(p))
print("a = " + str(a))
print("Calculated polynomial: ")
out = "f(x) = "
for i, an in enumerate(a[::-1]):
    index = len(a) - 1 - i
    if index == 1:
        out += str(an) + "x + "
    elif index != 0:
        out += str(an) + "x^" + str(index) + " + "
    else:
        out += str(an)
print(out)

print("----------------------------------")
print("Calculating shares")
for i in range(n):
    sum = 0
    for j, an in enumerate(a):
        sum += pow((i+1), j) * an
    sn.append(sum % p)

for i, key in enumerate(sn):
    print("s" + str(i + 1) + " = f(" + str(i) + ") mod " + str(p) + " = " + str(key))

shares = []
for i, si in enumerate(sn):
    share = {"x" : (i + 1), "y" : si}
    shares.append(share)

print("Coordinates: ")
for i, share in enumerate(shares):
    print(f"(x{i},y{i}) = ({share['x']},{share['y']})")

print("----------------------------------")
print("Secret recovery")
print("Select secrets: ")
decrypt_secrets = []
l = []
for i in range(t):
    sec = int(input())
    decrypt_secrets.append(sec)

for coordinate in decrypt_secrets:
    denom = 1
    num = 1
    xn = shares[coordinate - 1]["x"]
    for share in shares:
        if share["x"] in decrypt_secrets and share["x"] != coordinate:
            num *= -share["x"]
            denom *= (xn - share["x"])
    l.append(num / denom)

print("Free terms of calculated polynomials ln: ")
for n, ln in enumerate(l):
    print(f"l{n} = {format_result(ln)}")

print("Calculating the secret: ")
out = "s = ("
sum = 0
for n, ln in enumerate(l):
    result = sympy.Mod(ln*shares[decrypt_secrets[n] - 1]['y'], p)
    print(f"({shares[decrypt_secrets[n] - 1]['y']} * {format_result(ln)}) mod {p} = {format_result(result)}")
    sum += result
    out += str(format_result(result))
    if n != len(l) - 1:
        out += " + "
out += f") mod {p} = {format_result(sympy.Mod(sum, p))}"
print(out)