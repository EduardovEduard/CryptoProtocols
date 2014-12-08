__author__ = 'ees'

import numpy as np
import math

from functools import partial
from functools import reduce

from constants import *


def Pi(n, x):
    assert 0 <= Int(n, x) < 2 ** n, "WTF!!!"
    return Vec(n, PI_PERM[Int(n, x)])


Pi4 = partial(Pi, 4)
Pi8 = partial(Pi, 8)


def Vec(n, x):
    # assert math.ceil(math.log2(x)) <= n, "{} > {}".format(math.log2(x), n)
    result = np.zeros(n, int)
    binary = list(reversed(bin(x)[2:]))
    for i in range(len(binary)):
        result[result.size - i - 1] = int(binary[i])
    return result


Vec4 = partial(Vec, 4)
Vec8 = partial(Vec, 8)
Vec64 = partial(Vec, 64)

A = np.array([np.array(list(reversed(Vec64(int(x, 16))))) for x in A_list])  # Матрица с перевернутыми строчками


def Int(n, x):
    assert x.size == n, "{} != {}".format(x.size, n)
    num = 0
    for i, val in enumerate(reversed(x)):
        num += val * 2 ** i
    return int(num)


Int8 = partial(Int, 8)
Int4 = partial(Int, 4)


def Xor(x, y):
    return np.logical_xor(x, y).astype(int)


def Multiply(b):
    A_nonzero_rows = A[np.nonzero(b)]
    return reduce(Xor, A_nonzero_rows)


def S(a):
    assert len(a) == 512, "A must be of length 512"
    a_i = list(map(Int8, np.split(a, 64)))
    pi_i = list(map(Pi8, [Vec8(a_) for a_ in a_i]))
    return np.concatenate(pi_i)


def P(a):
    assert len(a) == 512, "A must be of length 512"
    a_i = list(map(Int8, np.split(a, 64)))
    tau_i = [Vec8(a_i[t]) for t in reversed(TAU)]
    return np.concatenate(tau_i)


# Bullshit
def L(a):
    assert len(a) == 512, "A must be of length 512"
    return a


def getK(K):
    ks = [K]
    k_next = K
    for i in range(1, len(C)):
        k_next = L(P(S(Xor(k_next, C[i]))))
        ks.append(k_next)
    return ks


def E(K, m):
    ks = list(reversed(getK(K)))
    tmp = m

    for i in range(11):
        tmp = L(P(S(Xor(ks[i], m))))
    return Xor(ks[11], tmp)


def compress(n, h, m):
    return Xor(Xor(E(L(P(S(Xor(h, n)))), m), h), m)


def gostHash(message, initVector = IV):
    h = initVector
    N = np.zeros(512)
    sigma = np.zeros(512)

    M = message
    while len(M) >= 512:
        m = M[-512:]
        h = compress(N, h, m)
        N = Vec(512, (Int(512, N) + 512) % 2 ** 512)
        sigma = Vec(512, (Int(512, sigma) + Int(512, m)) % 2 ** 512)
        M = M[:-512]

    size = 511 - len(M)
    zeros = np.zeros(size)
    m = np.concatenate((zeros, [1], M))
    h = compress(N, h, m)
    N = Vec(512, int((Int(512, N) + size) % 2 ** 512))
    sigma = Vec(512, int((Int(512, sigma) + Int(512, m)) % 2 ** 512))
    h = compress(np.zeros(512), h, N)
    h = compress(np.zeros(512), h, sigma)

    return h


def int_to_binary_array(x: int):
    size = x.bit_length()
    result = [0] * size

    for i in range(size):
        result[size - i - 1] = 1 if x & (1 << i) else 0

    return np.array(result)


def binary_array_to_int(x: np.array):
    sum = 0
    for i, num in enumerate(reversed(x)):
        sum += num * (2 ** i)
    return int(sum)


# if __name__ == '__main__':
#     M = 323130393837363534333231303938373635343332313039383736353433323130393837363534333231303938373635343332313039383736353433323130
#     G = 323130393837363534333231303938373635343332313039383736353433323130393837363534333231303938373635343332313039383736353433323131
#
#     message, m = int_to_binary_array(M), int_to_binary_array(G)
#     h = gostHash(message, IV)
#     g = gostHash(m, IV)
#
#     print(binary_array_to_int(h))
#     print(binary_array_to_int(g))