import math
import random
from termcolor import colored
from itertools import product

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

def f(state, i):
    theta(state)
    rho(state)
    pi(state)
    chi(state)
    iota(state, i)
    return state

def add_padding(message, r):
    padding_length = r - (len(message) % r)
    print(padding_length)
    for i in range(padding_length):
        if i == 0 or i == (padding_length - 1):
            message.append(1)
        else:
            message.append(0)
    return message

def hash(message, w, r):
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
    for i in range(permutations):
        for x, y, z in product(range(5), range(5), range(w)):
            state[x][y][z] = state[x][y][z] ^ message[bits_xored]
            bits_xored += 1
            if bits_xored % r == 0:
                break
        state = f(state, i)
    Z = []
    l = int(math.log2(w))
    # I co dalej?

def bitXYZ_sac(message, bit_x, bit_y, bit_z):
    w = len(message[0][0])
    hashed_message = hash(message)
    changed_message = []
    for x in range(5):
        temp1 = []
        for y in range(5):
            temp2 = []
            for z in range(w):
                if z == bit_z and y == bit_y and x == bit_x:
                    temp2.append(message[x][y][z] ^ 1)
                else:
                    temp2.append(message[x][y][z])
            temp1.append(temp2)
        changed_message.append(temp1)
    hashed_changed_message = hash(changed_message)
    print_matrix(message)
    print_matrix(hashed_message)
    print_matrix(changed_message)
    print_matrix(hashed_changed_message)
    bit_changed = 0
    for x in range(5):
        for y in range(5):
            for z in range(w):
                bit_changed += (hashed_message[x][y][z] ^ hashed_changed_message[x][y][z])
    return bit_changed

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

hash(message_bits, w, r)

message = []
for x in range(5):
    temp1 = []
    for y in range(5):
        temp2 = []
        for z in range(w):
            temp2.append(random.randint(0,1))
        temp1.append(temp2)
    message.append(temp1)

print("\nMessage: \n")
print_matrix(message)

hashed_message = hash(message)

print("Hashed message: \n")
print_matrix(hashed_message)

print(bitXYZ_sac(message, 0, 0, 0))