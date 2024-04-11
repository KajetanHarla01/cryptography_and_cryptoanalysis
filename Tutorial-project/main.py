from os import listdir
from hashlib import *
import random
from sympy import *
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import utils
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from os.path import isfile, join
import gmpy2
import os.path

def generate_keys_params(key_length=1024, e=65537):

    # Generate p and q
    p = random.getrandbits(key_length)
    q = random.getrandbits(key_length)
    p |= (1 << key_length - 1) | 1
    q |= (1 << key_length - 1) | 1

    # Make sure that p and q are prime numbers
    p = prevprime(p)
    q = nextprime(q)
    
    # Compute n and d
    n = p*q
    phi_n = (p-1)*(q-1)
    d = pow(e, -1, phi_n)

    public_numbers = rsa.RSAPublicNumbers(
        e=e,
        n=n
    )
    private_numbers = rsa.RSAPrivateNumbers(
        p=p,
        q=q,
        d=d,
        dmp1=d%(p-1),
        dmq1=d%(q-1),
        iqmp=pow(q, -1, p),
        public_numbers=public_numbers
    ).private_key(default_backend())

    return private_numbers, public_numbers

def calculate_file_sha3(filepath):
    file = open(filepath, "rb")
    s = sha3_256()
    s.update(file.read())
    return str.encode(s.hexdigest())

def get_file(dir):
    # Choose file from directory
    files = [f for f in listdir(dir) if isfile(join(dir, f))]
    if len(files)==0:
        print("Error: \"" + dir + "\" directory is empty")
        exit()
    
    print("Choose file: ")
    counter = 1
    for f in files:
        print(str(counter) + " - " + str(f))
        counter+=1
    file_choose = int(input("File number: "))
    if file_choose > len(files):
        print("Error: invalid file number")
        exit()
    return dir + "/" + files[file_choose - 1]

def get_private_numbers():
    path = "Tutorial-project/keys/private_key.pem"
    if not os.path.exists(path):
        print("Error: private key not found")
        exit()
    with open(path, "rb") as f:
        key_pem = f.read()
    private_key = serialization.load_pem_private_key(
        key_pem,
        password=None,
        backend=default_backend()
    )
    f.close()
    private_numbers = private_key.private_numbers()
    return private_numbers

def get_public_numbers():
    path = "Tutorial-project/keys/public_key.pem"
    if not os.path.exists(path):
        print("Error: public key not found")
        exit()
    with open(path, "rb") as f:
        key_pem = f.read()
    public_key = serialization.load_pem_public_key(
        key_pem,
        backend=default_backend()
    )
    f.close()
    public_numbers = public_key.public_numbers()
    return public_numbers

def generate_keys():

    # Generate keys
    private_numbers, public_numbers = generate_keys_params()
    print("Keys have been generated")
    
    # Write keys to file
    public_key_file = open("Tutorial-project/keys/public_key.pem", "wb")
    public_key = public_numbers.public_key(default_backend())
    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    public_key_file.write(public_key_pem)
    public_key_file.close()

    private_key_file = open("Tutorial-project/keys/private_key.pem", "wb")
    private_key_pem = private_numbers.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    private_key_file.write(private_key_pem)
    private_key_file.close()

def sign_file():
    # Get file from files directory
    filepath = get_file("Tutorial-project/files")  

    # Get file hash
    hash = calculate_file_sha3(filepath)

    # Sign the file hash
    private_key = get_private_numbers().private_key(default_backend())
    signature = private_key.sign(
        hash,
        padding.PKCS1v15(),
        hashes.SHA3_256()
    )

    # Write signature to .dat file
    sign_file_path = "Tutorial-project/signature/sign.dat"
    with open(sign_file_path, "wb") as sign_file:
        sign_file.write(signature)
    sign_file.close()
    print("File has been signed")

def check_signature():
    # Get signature file
    signature_file_path = "Tutorial-project/signature/sign.dat"
    if not os.path.exists(signature_file_path):
        print("Error: signature file not found")
        exit()
    with open(signature_file_path, "rb") as signature_file:
        signature = signature_file.read()

    # Get file from files directory
    filepath = get_file("Tutorial-project/files")

    # Calculate hash of the file
    file_hash = calculate_file_sha3(filepath)

    # Get public key
    public_key = get_public_numbers().public_key()

    # Verify the signature
    try:
        public_key.verify(
            signature,
            file_hash,
            padding.PKCS1v15(),
            hashes.SHA3_256()
        )
        print("Signature is valid.")
    except InvalidSignature:
        print("Signature is invalid.")
    
print("Choose program option: 1 - generate keys, 2 - sign file, 3 - check file signature")
opt = int(input())
if (opt == 1):
    generate_keys()
elif (opt == 2):
    sign_file()
elif (opt == 3):
    check_signature()
else:
    print("Error: Bad option number")