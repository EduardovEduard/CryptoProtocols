from random import randint

__author__ = 'ees'

import numpy as np

import random

from lab5 import gostHash, binary_array_to_int, int_to_binary_array
from lab3 import EllipticCurve

curve = EllipticCurve()

class Sign:
    def __init__(self, r, s):
        self.r = r
        self.s = s


def getE(alpha):
    e = alpha % curve.q
    return e if e != 0 else 1


def sign(d, message: np.array):
    Hash = gostHash(message)
    alpha = binary_array_to_int(Hash)
    e = getE(alpha)

    r = 0
    while r == 0:
        k = random.randint(1, curve.q - 1)
        C = curve.base_point * k
        r = C.x % curve.q

    s = (r * d + k * e) % curve.q

    s_vec = int_to_binary_array(s)
    r_vec = int_to_binary_array(r)
    return Sign(r_vec, s_vec)


def check(sign, message):
