# coding=utf-8

__author__ = 'ees'

import random

def powmod(a, p, m):
    """
    Процедура возведения a в степень p по модулю m,
    реализующая алгоритм быстрого возведения в степень
    :param a: Число, возводимое в степень
    :param p: Степень
    :param m: Модуль
    :return: A ^ P % M
    """
    accum = 1
    i = 0
    bpow2 = a
    while (p >> i) > 0:
        if (p >> i) & 1:
            accum = (accum * bpow2) % m
        bpow2 = (bpow2 * bpow2) % m
        i += 1
    return accum


def fact_mod(n, m):
    """
    Процедура вычисления факториала числа n по модулю m
    :param n: Аргумент факториала
    :param m: модуль
    :return: факториал по модулю m
    """
    tmp = 1
    for i in range(1, n + 1):
        tmp = (tmp * i) % m
    return tmp


def is_prime(n):
    """
    Процедура проверки числа на простоту, с помощью теоремы Вильсона
    :param n: Проверяемое число
    :return: результат проверки на простоту
    """
    if n <= 1:
        return False
    return fact_mod(n - 1, n) == n - 1


class GOSTGenerator:
    """
    Класс, реализующий алгоритм генерации параметров p, q, a по ГОСТ-34.10-94
    """
    @staticmethod
    def __calculate_t(t0=510):
        """
        Генерация списка размеров T
        :param t0: Максимальный размер числа
        :return: список размеров T
        """

        t = [t0]

        while t[-1] >= 17:
            t.append(t[-1] // 2)
        s = len(t)
        return t, s


    @staticmethod
    def __next_prime(s):
        """
        Процедура получения наименьшего простого числа заданного размера
        :param s: Размер получаемого числа в битах
        :return: Наименьшее простое число заданного размера
        """
        if s <= 0:
            raise RuntimeError('NextPrime: S should be greater than zero!')

        tmp = 2 ** (s - 1) + 1
        while not is_prime(tmp):
            tmp += 2
        return tmp


    @staticmethod
    def __generate_z(y0, c, size):
        """
        Процедура генерации промежуточного параметра Z
        :param y0: Начальное значение последовательности y
        :param c: Параметр генерации c
        :param size: размер последовательности
        :return: Z, X0
        """

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
        """
        Процедура A
        :param x0: Первый параметр конгруэнтного генератора
        :param c: Второй параметр конгруэнтного генератора
        :param t: Битность генерируемого числа p 510 <= t <= 512
        :return: Сгенерированные числа p, q
        """
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
            d, r = divmod(t_list[m - 1], 16)
            rm = d if r == 0 else d + 1

            p[m - 1] = 2 ** (t + 1)  # Дабы цикл отработал хотя бы разок
            while p[m - 1] > 2 ** t:
                z, y0 = self.__generate_z(y0, c, rm)

                left_d, left_r = divmod(2 ** (t_list[m - 1] - 1), p[m])
                left_part = left_d if left_r == 0 else left_d + 1

                right_d, right_r = divmod(2 ** (t_list[m - 1] - 1) * z, p[m] * 2 ** (16 * rm))
                right_part = right_d if right_r == 0 else right_d + 1

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


    @staticmethod
    def __c(p, q):
        """
        Процедура C
        :param p: Сгенерированное процедурой A число P
        :param q: Сгенерированное процедурой A число Q
        :return: Число \alpha: \alpha ^ q mod p = 1
        """
        a = 1
        while a == 1:
            d = random.randint(2, p - 2)
            a = powmod(d, (p - 1) // q, p)
        return a


    def generate_p_q_a(self, t):
        """
        Процедура генерации p, q, a
        :param t: Битность p
        :return: p, q, a
        """
        x0 = random.randint(0, 2 ** 16 - 1)
        c = random.randint(0, 2 ** 16 - 1)
        p, q = self.__a(x0, c, t)
        alpha = self.__c(p, q)
        return p, q, alpha


if __name__ == '__main__':
    generator = GOSTGenerator()
    p, q, a = generator.generate_p_q_a(510)
    print(powmod(a, q, p) == 1)