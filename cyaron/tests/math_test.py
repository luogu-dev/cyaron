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

        for i in range(20):
            n = randint(1, self.prime_range)
            self.assertEqual(nextprime(n), bf_nextprime(n))
            self.assertEqual(nextprime(i), bf_nextprime(i))

    def test_prevprime(self):

        def bf_prevprime(n):
            while True:
                n -= 1
                if n in self.prime_set:
                    return n
                if n < 2:
                    return 0

        for i in range(20):
            n = randint(1, self.prime_range)
            self.assertEqual(prevprime(n, False), bf_prevprime(n))
            self.assertEqual(prevprime(i, False), bf_prevprime(i))

        self.assertRaises(ValueError, prevprime, 1)
        self.assertRaises(ValueError, prevprime, 2)
