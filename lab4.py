__author__ = 'ees'

from Crypto.Util.number import inverse

import numpy as np
import unittest

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
    s = 0
    while r == 0 and s == 0:
        k = random.randint(1, curve.q - 1)
        C = curve.base_point * k
        r = C.x % curve.q
        s = (r * d + k * e) % curve.q

    Q = curve.base_point * d
    return Sign(r, s), Q


def check(sign, Q, message):

    r = sign.r
    s = sign.s

    if 0 < r < curve.q and 0 < s < curve.q:

        hash = gostHash(message)
        alpha = binary_array_to_int(hash)
        e = getE(alpha)
        v = inverse(e, curve.q)
        z1 = (s * v) % curve.q
        z2 = (-r * v) % curve.q

        C = (curve.base_point * z1) + (Q * z2)
        R = C.x % curve.q
        return R == r

    else:
        return False


class SignTest(unittest.TestCase):
    def test_group_property(self):
        c = EllipticCurve()
        for i in range(100):
            a = random.randint(1, c.q - 1)
            self.assertEqual(c.base_point * (c.q + a), c.base_point * a)

    def test_check(self):
        c = EllipticCurve()
        for i in range(10):
            message = int_to_binary_array(random.randint(10 ** 10, 10 ** 20))
            d = random.randint(0, c.q)
            sign_, Q = sign(d, message)
            self.assertTrue(check(sign_, Q, message))