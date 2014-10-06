from lab1 import *
import random
import hashlib
from Crypto.Util.number import *

__author__ = 'ees'

generator = GOSTGenerator()
p, q, a = generator.generate_p_q_a(512)
x = random.randint(1, q - 1)
y = powmod(a, x, q)

def getHash(message):
    message = message.encode()
    hasher = hashlib.sha256()
    hasher.update(message)
    H = int(hasher.hexdigest(), 16)
    return H

def generate(message):
    S = 0
    while S == 0:
        k = random.randint(2, q - 1)
        R = powmod(a, k, p) % q
        H = getHash(message)
        S = (k * H + x * R) % q
    return R, S


def check(message, R, S):
    if R >= q or S >= q:
        return False

    H = getHash(message)
    H_inv = inverse(H, p)
    Hy_inv = inverse(H * y, p)
    R_check = (powmod(a, S, p) - )
    print(R)
    print(R_check)
    return R == R_check

message = "Hello world!"
R, S = generate(message)
print(check(message, R, S))