__author__ = 'ees'

from Crypto.Util.number import inverse

import doctest


def fast_multiply(p, scalar):
    """
    >>> powmod(55, 100)
    5500
    >>> powmod(600000000000000000000, 10000000000000000000000000)
    6000000000000000000000000000000000000000000000
    """
    accum = None if isinstance(p, EllipticPoint) else 0
    tmp = p
    i = 0
    while scalar >> i > 0:
        if scalar >> i & 1:
            accum = tmp + accum
        tmp = tmp + tmp
        i += 1
    return accum


class EllipticPoint:
    def __init__(self, x, y, curve):
        self.x = x
        self.y = y
        self.curve = curve

    def get_lambda(self, other):
        p = self.curve.p
        if self.x != other.x:
            return ((other.y - self.y) * inverse(other.x - self.x, p)) % p
        else:
            return ((3 * self.x ** 2 + self.curve.a) * inverse(2 * self.y, p)) % p

    def __add__(self, other):
        if other is None:
            return self

        if self.is_subject_to_be_zero_point(other):
            raise ValueError('Wtf? Zero point!')

        p = self.curve.p
        lambda_ = self.get_lambda(other)

        x = (lambda_ ** 2 - self.x - other.x) % p
        y = (lambda_ * (self.x - x) - self.y) % p

        return EllipticPoint(x, y, self.curve)

    def __mul__(self, scalar: int):
        assert isinstance(scalar, int)
        return fast_multiply(self, scalar)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.curve is other.curve

    def __str__(self):
        return "X: {}, Y: {}".format(self.x, self.y)

    def is_subject_to_be_zero_point(self, other):
        return self.x == other.x and self.y == self.curve.p - other.y and self.curve is other.curve


class EllipticCurve:
    def __init__(self, **params):
        self.params = params or {'a': "FFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFC",
                                 'b': "5AC635D8AA3A93E7B3EBBD55769886BC651D06B0CC53B0F63BCE3C3E27D2604B",
                                 'm': "FFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551",
                                 'q': "FFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551",
                                 'p': "FFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFF",
                                 'P': {'x': "6B17D1F2E12C4247F8BCE6E563A440F277037D812DEB33A0F4A13945D898C296",
                                       'y': "4FE342E2FE1A7F9B8EE7EB4A7c0F9E162BCE33576B315ECECBB6406837BF51F5"}}

        self.a = int(self.params['a'], 16)
        self.b = int(self.params['b'], 16)
        self.m = int(self.params['m'], 16)
        self.q = int(self.params['q'], 16)
        self.p = int(self.params['p'], 16)
        self.P_x = int(self.params['P']['x'], 16)
        self.P_y = int(self.params['P']['y'], 16)

        # self.a = 0
        # self.b = 7
        # self.p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
        # self.P_x = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
        # self.P_y = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
        # self.q = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
        self.n = 1

        self.base_point = EllipticPoint(self.P_x, self.P_y, self)

doctest.testmod()
