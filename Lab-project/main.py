import math
import random

def print_state(state):
    for z in range(len(state[0][0])):
        print(f"for z = {z}: ")
        for y in range(5):
            out = ""
            for x in range(5):
                out += f"{state[x][y][z]} "
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

def rho(state, rho_const):
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

def pi(state, pi_const):
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

b_tab = [25, 50, 100, 200, 400, 800, 1600]
print("Choose b value ")
for i, b in enumerate(b_tab):
    print(f"{i+1}) {b}")
choice = int(input("Choose element number: "))
b = b_tab[choice - 1]
w = int(b/25)
l = int(math.log2(w))
print(f"b = {b} | w = {w} | l = {l}")

rho_const = [3, 21, 11, 28, 0, 1, 6, 25, 8, 18, 14, 27, 24, 2, 4, 13, 7, 23, 20, 12, 9, 10, 15, 17, 19]
pi_const = [3, 2]

state = []
for x in range(5):
    temp1 = []
    for y in range(5):
        temp2 = []
        for z in range(w):
            temp2.append(random.randint(0,1))
        temp1.append(temp2)
    state.append(temp1)

print("State array before permutations")
print()
print_state(state)

permutations = 12 + (2 * l)
for i in range(permutations):
    theta(state)
    rho(state, rho_const)
    pi(state, pi_const)
    chi(state)
    iota(state, i) 
       
print("State array after permutations")
print()
print_state(state)