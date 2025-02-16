import unittest
from random import randint
from cyaron import randprime, nextprime, prevprime, prime_sieve


class TestMath(unittest.TestCase):

    def setUp(self):
        self.prime_range = 100000
        self.prime_set = set(prime_sieve(self.prime_range * 2))
        return super().setUp()

    def test_randprime(self):
        for _ in range(20):
            self.assertTrue(randprime(1, self.prime_range) in self.prime_set)

    def test_nextprime(self):

        def bf_nextprime(n):
            while True:
                n += 1
                if n in self.prime_set:
                    return n

        for _ in range(20):
            n = randint(1, self.prime_range)
            self.assertEqual(nextprime(n), bf_nextprime(n))

    def test_prevprime(self):

        def bf_prevprime(n):
            while True:
                n -= 1
                if n in self.prime_set:
                    return n
                if n < 2:
                    return 0

        for _ in range(20):
            n = randint(1, self.prime_range)
            self.assertEqual(prevprime(n, False), bf_prevprime(n))

        self.assertRaises(ValueError, prevprime, 1)
        self.assertRaises(ValueError, prevprime, 2)
        self.assertEqual(prevprime(1, False), 0)
        self.assertEqual(prevprime(2, False), 0)
