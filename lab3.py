__author__ = 'ees'

from Crypto.Util.number import inverse


def powmod(p, scalar):
    accum = None
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
        assert self.curve is other.curve, "Points must lie on same curve"

        p = self.curve.p
        if self.x != other.x:
            return ((other.y - self.y) * inverse(other.x - self.x, p)) % p
        else:
            return ((3 * self.x ** 2 + self.curve.a) * inverse(2 * self.y, p)) % p

    def __add__(self, other):
        if other is None:
            return self

        assert self.curve is other.curve, "Points must lie on same curve"

        if self.is_subject_to_be_zero_point(other):
            raise ValueError('Wtf? Zero point!')

        p = self.curve.p
        lambda_ = self.get_lambda(other)

        x = (lambda_ ** 2 - self.x - other.x) % p
        y = (lambda_ * (self.x - x) - self.y) % p

        return EllipticPoint(x, y, self.curve)

    def __mul__(self, scalar: int):
        assert isinstance(scalar, int)
        return powmod(self, scalar)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.curve is other.curve

    def __str__(self):
        return "X: {}, Y: {}".format(self.x, self.y)

    def is_subject_to_be_zero_point(self, other):
        return self.x == other.x and self.y == self.curve.p - other.y and self.curve is other.curve


class EllipticCurve:
    def __init__(self):
        self.a = 0
        self.b = 7
        self.p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
        self.P_x = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
        self.P_y = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
        self.q = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
        self.n = 1

        self.base_point = EllipticPoint(self.P_x, self.P_y, self)


curve = EllipticCurve()
point = curve.base_point
