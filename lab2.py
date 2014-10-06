from lab1 import *
import random
import hashlib
from Crypto.Util.number import *

__author__ = 'ees'

generator = GOSTGenerator()
p, q, a = generator.generate_p_q_a(512)
x = random.randint(1, q - 1)
y = powmod(a, x, p)

def get_hash(message):
    message = message.encode()
    hasher = hashlib.sha256()
    hasher.update(message)
    H = int(hasher.hexdigest(), 16)
    return H

def generate(message):
    S = 0
    while S == 0:
        k = random.randint(2, q - 1)
        R = powmod(a, k, p)
        R_ = R % q
        H = get_hash(message)
        S = (k * H + x * R_) % q
    return R_, S


def check(message, R, S):
    if R >= q or S >= q:
        return False

    H = get_hash(message)
    v = powmod(H, q - 2, q)
    z1 = (S * v) % q
    z2 = ((q - R) * v) % q
    u = ((powmod(a, z1, p) * powmod(y, z2, p)) % p) % q
    print(R)
    print(u)
    return R == u


message = "Hello world!"
R, S = generate(message)
print(check(message, R, S))