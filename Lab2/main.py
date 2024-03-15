import random
k = int(input("Input k: "))
s = int(input("Input s in range(0," + str(k-1) +"): "))
n = int(input("Input n: "))
sn = []

for i in range(n-1):
    val = random.randint(0,k-1)
    sn.append(val)

sn.append((s - sum(sn)) % k)
print("sn = " + str(sn))
print("Decrypted s = " + str(sum(sn)%k))
