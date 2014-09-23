# coding=utf-8

__author__ = 'ees'

import random
import math


def powmod(b, e, n):
    accum = 1
    i = 0
    bpow2 = b
    while (e >> i) > 0:
        if (e >> i) & 1:
            accum = (accum * bpow2) % n
        bpow2 = (bpow2 * bpow2) % n
        i += 1
    return accum


def fact_mod(n, m):
    tmp = 1
    for i in range(1, n + 1):
        tmp = (tmp * i) % m
    return tmp


def is_prime(n):
    if n <= 1:
        return False
    return fact_mod(n - 1, n) == n - 1


class GOSTGenerator:

    @staticmethod
    def __calculate_t(t0=510):

        t = [t0]

        while t[-1] >= 17:
            t.append(t[-1] // 2)
        s = len(t)
        return t, s


    @staticmethod
    def __next_prime(s):
        if s <= 0:
            raise RuntimeError('NextPrime: S should be greater than zero!')

        tmp = 2 ** (s - 1) + 1
        while not is_prime(tmp):
            tmp += 2
        return tmp


    @staticmethod
    def __generate_z(y0, c, size):
        if size <= 0:
            raise RuntimeError("Generate Z: size should be greater than zero!")
        y = [y0] * size
        for i in range(1, size):
            y[i] = (19381 * y[i - 1] + c) % 2 ** 16

        tmp = 0
        for i in range(size - 1):
            tmp += y[i] * (2 ** (16 * i))
        return tmp, y[-1]


    def __a(self, x0, c, t):
        if c >= 2 ** 16 or c <= 0 or \
           x0 >= 2 ** 16 or x0 <= 0:
              return -1

        t_list, s = self.__calculate_t(t)
        p_s = self.__next_prime(t_list[s - 1])
        p = [0] * s
        p[-1] = p_s
        m = s - 1
        y0 = x0

        while m > 0:
            rm = math.ceil(t_list[m - 1] / 16)

            p[m - 1] = 2 ** (t + 1)
            while p[m - 1] > 2 ** t:
                z, y0 = self.__generate_z(y0, c, rm)
                left_part = math.ceil(2 ** (t_list[m - 1] - 1) / p[m])
                right_part = math.floor((2 ** (t_list[m - 1] - 1) * z) / (p[m] * 2 ** (16 * rm)))
                N = left_part + right_part
                N = N if N % 2 == 0 else N + 1

                k = 0
                p_is_good = False
                while not p_is_good:
                    p[m - 1] = p[m] * (N + k) + 1

                    a_value = powmod(2, p[m] * (N + k), p[m - 1])
                    b_value = powmod(2, N + k, p[m - 1])

                    if p[m - 1] > 2 ** t:
                        break
                    elif (a_value == 1) and (b_value != 1):
                        p_is_good = True
                    else:
                        k += 2
            m -= 1
        return p[0], p[1]


    def __c(self, p, q):
        f = 1
        while f == 1:
            d = random.randint(2, p - 2)
            f = powmod(d, (p - 1) // q, p)
        return f


    def generate_p_q_a(self, t):
        x0 = random.randint(0, 2 ** 16 - 1)
        c = random.randint(0, 2 ** 16 - 1)
        p, q = self.__a(x0, c, t)
        alpha = self.__c(p, q)
        return (p, q, alpha)

if __name__ == '__main__':
    generator = GOSTGenerator()
    p, q ,a = generator.generate_p_q_a(510)
    print(powmod(a, q, p) == 1)