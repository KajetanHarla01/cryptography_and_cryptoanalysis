import itertools
import random
file_name = "sbox_08x08.SBX"
data = []
with open(file_name, 'rb') as f:
    i = 0
    while True:
        byte_s = f.read(1)
        if not byte_s:
            break
        byte = byte_s[0]
        if i%2 == 0:
            data.append(byte)
        i+=1
f = []
x = []
for i in range(0,8):
    bits = []
    for byte in data:
        bits.append((byte >> i) & 1)
    f.append(bits)
print("Checking the balance:")
balanced = True
for i in range(0,8):
    print("f" + str(i) + ": ones " + str(sum(f[i])) + " | zeros " + str(256 - sum(f[i])))
    if sum(f[i]) != (256 - sum(f[i])):
        balanced = False
if balanced:
    print("All f functions are balanced")
else:
    print("Not all f functions are balanced")
for i in range(0,8):
    tmp = []
    for j in range(0,256):
        tmp.append((j >> i) & 1)
    x.append(tmp)
base_functions = {0,1,2,3,4,5,6,7}
for i in range(2,9):
    combinations = list(itertools.combinations(base_functions, i))
    for comb in combinations:
        func = []
        for j in range(0, 256):
            temp_bit = x[comb[0]][j]
            for k in range(1, len(comb)):
                temp_bit ^= x[comb[k]][j]
            func.append(temp_bit)
        x.append(func)
x.append([0]*256)
for i in range(0, len(x)):
    temp = []
    for j in range(0, 256):
        temp.append(x[i][j] ^ 1)
    x.append(temp)
print("\nThe size of the set of linear functions: " + str(len(x)))
distance = []
for i in range(0,8):
    temp_d = []
    for func in x:
        d = 0
        for j in range(0, 256):
            d += func[j] ^ f[i][j]
        temp_d.append(d)
    distance.append(temp_d)
print("\nMinD of f functions: ")
for i in range(0, len(distance)):
    print("minD(f" + str(i) + ", LF) = " + str(min(distance[i])))
print("\nChecking SAC of the functions:")
num = 0
all_sac = 0
for func in f:
    sac = 0
    for i in range(0, 8):
        ones = 0
        for j in range(0, 256):
            alpha = pow(2, i)
            index = j ^ alpha
            ones += func[index] ^ func[j]
        sac += ones/256
    print("SAC f" + str(num) + " = " + str(sac/8))   
    all_sac += sac/8   
    num += 1
print("SAC = " + str(all_sac/8))
nums = list(range(256))
inputComb = list(itertools.combinations(nums, 2))
xor_profile = []
for i in range(0, 256):
    xor_profile.append([0]*256)
show = True
for comb in inputComb:
    input = comb[0] ^ comb[1]
    output = data[comb[0]] ^ data[comb[1]]
    xor_profile[input][output] += 2
print("\nMax XOR profile = " + str(max(map(max, xor_profile))))
print("\nChecking cycles:")
value = random.randint(0, 255)
used_values = []
cycles = 0
while True:
    cycles += 1
    while data[value] not in used_values:
        value = data[value]
        used_values.append(value)
    if len(used_values) < 256:
        value = random.choice(list(set(range(256)) - set(used_values)))
    else:
        break
print("Cycles count = " + str(cycles))    