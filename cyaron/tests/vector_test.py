import unittest
from cyaron.vector import *


def has_duplicates(lst: list):
    return len(lst) != len(set(lst))


class TestVector(unittest.TestCase):

    def test_unique_vector(self):
        v = Vector.random(10**5, [10**6])
        self.assertFalse(has_duplicates(list(map(lambda tp: tuple(tp), v))))
        self.assertTrue(all(map(lambda v: 0 <= v[0] <= 10**6, v)))
        v = Vector.random(1000, [(10**5, 10**6)])
        self.assertTrue(all(map(lambda v: 10**5 <= v[0] <= 10**6, v)))
        with self.assertRaises(
                Exception,
                msg=
                "1st param is so large that CYaRon can not generate unique vectors",
        ):
            v = Vector.random(10**5, [10**4])

    def test_repeatable_vector(self):
        v = Vector.random(10**5 + 1, [10**5], VectorRandomMode.repeatable)
        self.assertTrue(all(map(lambda v: 0 <= v[0] <= 10**5, v)))
        self.assertTrue(has_duplicates(list(map(lambda tp: tuple(tp), v))))
        v = Vector.random(1000, [(10**5, 10**6)], VectorRandomMode.repeatable)
        self.assertTrue(all(map(lambda v: 10**5 <= v[0] <= 10**6, v)))

    def test_float_vector(self):
        v = Vector.random(10**5, [10**5], VectorRandomMode.float)
        self.assertTrue(all(map(lambda v: 0 <= v[0] <= 10**5, v)))
        v = Vector.random(10**5, [(24, 25)], VectorRandomMode.float)
        self.assertTrue(all(map(lambda v: 24 <= v[0] <= 25, v)))
