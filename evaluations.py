import random
import math
import datetime
from random_evaluator import evaluate
from binascii import hexlify

class SequenceGenerator(object):
    def __init__(self):
        self.seed()

    def seed(self):
        pass

    def getrandbits(self, k):
         return ''.join(self.randbyte() for _ in range(k / 8))

class Linear(SequenceGenerator):
    def __init__(self):
        self._direction = 1
        self._next = 0

    def seed(self):
        self._next = 0
        self._direction = self._direction * -1

    def randbyte(self):
        byte = chr(self._next)
        self._next = (self._next + 1) % 256
        return byte

class Sine(SequenceGenerator):
    def seed(self):
        self._next = 0

    def randbyte(self):
        byte = chr(int(math.sin(self._next) + 1) * 128)
        self._next += 1
        return byte

class CurrentTime(SequenceGenerator):
    def randbyte(self):
        return chr(datetime.datetime.now().microsecond % 256)

class CurrentTimePeriodic(SequenceGenerator):
    def randbyte(self):
        return chr(int(math.sin(datetime.datetime.now().microsecond) + 1) * 128)

class BiasedPseudoRandom(SequenceGenerator):
    def __init__(self, reduction_factor=1):
        self.range_max = (2**8 / reduction_factor) - 1

    def seed(self):
        random.seed()

    def randbyte(self):
        return chr(random.randint(0, self.range_max))

class StaticRandomSet(SequenceGenerator):

    def __init__(self, size):
        self._static_set = []
        for _ in range(size):
            self._static_set.append(random.randint(0, 255))
        self.seed()

    def seed(self):
        self._next = 0

    def randbyte(self):
        self._next += 1
        return chr(self._static_set[self._next % len(self._static_set)])

class SystemRandom(SequenceGenerator):
    def seed(self):
        self._random = random.SystemRandom()

    def randbyte(self):
        return chr(self._random.randint(0, 255))


evaluate("Sine", Sine())
evaluate("Linear", Linear())
evaluate("Current Time Periodic", CurrentTimePeriodic())
evaluate("Current Time", CurrentTime())
evaluate("Static random set", StaticRandomSet(2**15))

for k in range(8, -1, -1):
    evaluate("Python random biased (reduce range by 2^%d)" % k, BiasedPseudoRandom(2**k))

evaluate("System random", SystemRandom())
