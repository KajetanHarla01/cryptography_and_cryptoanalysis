import random
import sympy
from sympy.solvers import solve
from sympy import Symbol
s = 328 #int(input("Input s: "))
n = 4 #int(input("Input n: "))
t = 3 #int(input("Input t: "))
sn = []
a = []

a.append(s)
min_p = (s if s > n else n)  + 1
prime_num = random.randint(0, 20)
p = sympy.nextprime(min_p)
for i in range(prime_num):
    p = sympy.nextprime(min_p)
    min_p = p

print("p = " + str(p))
for i in range(t - 1):
    a.append(random.randint(1, 1000))

print("a = " + str(a))

for i in range(4):
    sum = 0
    for j, an in enumerate(a):
        sum += pow((i+1), j) * an
    sn.append(sum % p)

print("sn = " + str(sn))

decrypt_secrets = {0,1,3} #[]

#for i in range(t):
#    sec = int(input("Secret number to decrypt: "))
#    decrypt_secrets.append(sec)

symbols = []
for sec in decrypt_secrets:
    symbols.append(Symbol("a" + str(sec)))

equations = []
for i in range(t):
    for a in symbols:
        sympy.Eq()