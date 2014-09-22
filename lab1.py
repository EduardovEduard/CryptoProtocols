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


def calculate_t(t0=510):
    t = [t0]

    while t[-1] >= 17:
        t.append(t[-1] // 2)
    s = len(t)
    return t, s


def fact_mod(n, m):
    tmp = 1
    for i in range(1, n + 1):
        tmp = (tmp * i) % m
    return tmp


def is_prime(n):
    if n <= 1:
        return False
    return fact_mod(n - 1, n) == n - 1


def next_prime(s):
    tmp = 2 ** (s - 1) + 1
    while not is_prime(tmp):
        tmp += 2
    return tmp


def generate_z(y0, c, size):
    y = [y0] * size
    for i in range(1, size):
        y[i] = (19381 * y[i - 1] + c) % 2 ** 16

    tmp = 0
    for i in range(size - 1):
        tmp += y[i] * (2 ** (16 * i))
    return tmp, y[-1]


def a(x0, c, t):
    if c >= 2 ** 16 or c <= 0 or \
       x0 >= 2 ** 16 or x0 <= 0:
        return -1

    t_list, s = calculate_t(t)
    p_s = next_prime(t_list[s - 1])
    p = [0] * s
    p[-1] = p_s
    m = s - 1
    y0 = x0

    while m > 0:
        rm = math.ceil(t_list[m - 1] / 16)

        p[m - 1] = 2 ** (t + 1)
        while p[m - 1] > 2 ** t:
            z, y0 = generate_z(y0, c, rm)
            N = math.ceil(2 ** (t_list[m - 1] - 1) / p[m]) + \
                math.floor((2 ** (t_list[m - 1] - 1) * z) / (p[m] * 2 ** (16 * rm)))
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


def c(p, q):
    f = 1
    while f == 1:
        d = random.randint(2, p - 2)
        f = powmod(d, (p - 1) // q, p)
    return f


def generate_p_q_a(x0, c, t):
    p, q = a(x0, c, t)
    alpha = c(p, q)
    return (p, q, alpha)