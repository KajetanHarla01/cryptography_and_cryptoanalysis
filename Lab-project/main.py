import math
from itertools import *

def print_matrix(matrix):
    for z in range(len(matrix[0][0])):
        print(f"for z = {z}: ")
        for y in range(5):
            out = ""
            for x in range(5):
                out += f"{matrix[x][y][z]} "
            print(out)
        print()

def theta(state):
    w = len(state[0][0])
    for z in range(w):
        pairity = []
        for y in range(5):
            xor = 0
            for x in range(5):
                xor ^= state[x][y][z]
            pairity.append(xor)
        for x in range(5):
            for y in range(5):
                state[x][y][z] = state[x][y][z] ^ pairity[(x - 1) % 5] ^ pairity[(x + 1) % 5]

def rho(state):
    rho_const = [153, 55, 28, 120, 21, 231, 276, 91, 78, 136, 3, 36, 0, 210, 105, 10, 300, 1, 66, 45, 171, 6, 190, 253, 15]
    w = len(state[0][0])
    temp_tabs = []
    for x in range(5):
        for y in range(5):
            temp = []
            for z in range(w):
                temp.append(state[x][y][z])
            temp_tabs.append(temp)
    for x in range(5):
        for y in range(5):
            for z in range(w):
                state[x][y][z] = temp_tabs[x*5 + y][(z + rho_const[x*5 + y]) % w]

def pi(state):
    pi_const = [1, 3]
    w = len(state[0][0])
    for z in range(w):
        temp_tabs = []
        for y in range(5):
            temp = []
            for x in range(5):
                temp.append(state[x][y][z])
            temp_tabs.append(temp)
        for x in range(5):
            for y in range(5):
                state[x][y][z] = temp_tabs[(pi_const[0]*y + pi_const[1]*x) % 5][y]

def chi(state):
    w = len(state[0][0])
    for z in range(w):
        temp_tabs = []
        for y in range(5):
            temp = []
            for x in range(5):
                temp.append(state[x][y][z])
            temp_tabs.append(temp)
        for x in range(5):
            for y in range(5):
                state[x][y][z] = temp_tabs[y][x] ^ (~temp_tabs[(y + 1) % 5][x] & temp_tabs[(y + 2) % 5][x])

def rc(t):
    if t % 255 == 0:
        return 1
    R = [0,0,0,0,0,0,0,1]
    for i in range(1, t % 255 + 1):
        R.append(0)
        R[0] = R[0] ^ R[8]
        R[4] = R[4] ^ R[8]
        R[5] = R[5] ^ R[8]
        R[6] = R[6] ^ R[8]
        R = R[0:8]
        del R[8:]
    return R[0]

def iota(state, i):
    w = len(state[0][0])
    RC = [0] * w
    for j in range(int(math.log2(w)) + 1):
        RC[pow(2, j) - 1] = rc(j + 7*i)
    temp = []
    for z in range(w):
        state[0][0][z] = state[0][0][z] ^ RC[z]

def f(state, l):
    perm = 12 + 2*l
    for i in range(perm):
        theta(state)
        rho(state)
        pi(state)
        chi(state)
        iota(state, i)
    return state

def add_padding(message, r):
    padding_length = r - (len(message) % r)
    for i in range(padding_length):
        if i == 0 or i == (padding_length - 1):
            message.append(1)
        else:
            message.append(0)
    return message

def hash(message, w, r, hash_len = 256):
    state = []
    for x in range(5):
        temp1 = []
        for y in range(5):
            temp2 = []
            for z in range(w):
                temp2.append(0)
            temp1.append(temp2)
        state.append(temp1)
    message = add_padding(message, r)
    bits_xored = 0
    permutations = int(len(message) / r)
    l = int(math.log2(w))
    for i in range(permutations):
        for x, y, z in product(range(5), range(5), range(w)):
            state[x][y][z] = state[x][y][z] ^ message[bits_xored]
            bits_xored += 1
            if bits_xored % r == 0:
                break
        state = f(state, l)
    Z = []
    counter = 0
    for x, y, z in product(range(5), range(5), range(w)):
        Z.append(state[x][y][z])
        counter += 1
        if counter > r:
            break
    while len(Z) < hash_len:
        state = f(state, l)
        counter = 0
        for x, y, z in product(range(5), range(5), range(w)):
            Z.append(state[x][y][z])
            counter += 1
            if counter > r:
                break
    return Z[:hash_len]

def sac(message_bits, w, r, hash_len=256):
    hashed = hash(message_bits, w, r)
    sac_sum = 0
    for i in range(len(message_bits)):
        comp_tab = []
        for j, bit in enumerate(message_bits):
            if i != j:
                comp_tab.append(bit)
            else:
                comp_tab.append(bit^1)
        comp_hash = hash(comp_tab, w, r)
        xor = 0
        for j in range(len(hashed)):
            xor += hashed[j] ^ comp_hash[j]
        sac_sum += (float)(xor/len(hashed))
    return (float)(sac_sum / len(message_bits))

b_tab = [25, 50, 100, 200, 400, 800, 1600]
print("Choose b value ")
for i, b in enumerate(b_tab):
    print(f"{i+1}) {b}")
choice = int(input("Choose element number: "))
b = b_tab[choice - 1]
w = int(b/25)
l = int(math.log2(w))
print(f"b = {b} | w = {w} | l = {l}")

message = input("Input message to hash: ")
r = int(input("Input block size r:"))
message_bits = []
for char in message:
    for bit in bin(ord(char))[2:].zfill(8):
        message_bits.append(int(bit))

hashed = hash(message_bits, w, r)
hash_bytes = [sum([byte[b] << b for b in range(0,8)])
            for byte in zip(*(iter(hashed),) * 8)
        ]
hash_hex = ''.join('{:02x}'.format(x) for x in hash_bytes)

print(f"\nMessage: {message}" )
print(f"\nHashed message: {hash_hex}")
print(f"\nSAC: {sac(message_bits, w, r)}")