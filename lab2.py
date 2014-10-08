from lab1 import *
import random
import hashlib

__author__ = 'ees'

class Gost1994Sign:

    def __init__(self, generator=None, hash_function=None):
        if generator is None:
            self.generator = GOSTGenerator()

        self.p, self.q, self.a = self.generator.generate_p_q_a(512)
        self.x = random.randint(1, self.q - 1)
        self.y = powmod(self.a, self.x, self.p)

    @staticmethod
    def get_hash(message):
        message = message.encode()
        hasher = hashlib.sha256()
        hasher.update(message)
        H = int(hasher.hexdigest(), 16)
        return H

    def generate(self, message):
        S = 0
        while S == 0:
            k = random.randint(2, self.q - 1)
            R = powmod(self.a, k, self.p)
            R_ = R % self.q
            H = self.get_hash(message) % self.q
            S = (k * H + self.x * R_) % self.q
        return R_, S


    def check(self, message, R, S):
        if R >= self.q or S >= self.q:
            return False

        H = self.get_hash(message) % self.q
        v = powmod(H, self.q - 2, self.q)
        z1 = (S * v) % self.q
        z2 = ((self.q - R) * v) % self.q
        u = ((powmod(self.a, z1, self.p) * powmod(self.y, z2, self.p)) % self.p) % self.q
        return R == u


message = "Я тестовое сообщение" * 20
gen = Gost1994Sign()
print('Сгенерированные параметры:')
print('\tp = {}'.format(gen.p))
print('\tq = {}'.format(gen.q))
print('\ta = {}'.format(gen.a))

R, S = gen.generate(message)

print('\tR = {}'.format(R))
print('\tS = {}'.format(S))

print("Подпись действительна: {}".format(gen.check(message, R, S)))