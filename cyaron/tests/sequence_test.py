import unittest
from cyaron import Sequence


class TestSequence(unittest.TestCase):

    def test_simple_get_one(self):
        seq = Sequence(lambda i, f: 2 * i + 3)
        self.assertEqual(seq.get(1), 5)
        self.assertEqual(seq.get(5), 13)

    def test_simple_get_many(self):
        seq = Sequence(lambda i, f: 3 * i + 2)
        self.assertEqual(seq.get(1, 3), [5, 8, 11])

    def test_func_get_one(self):
        seq = Sequence(lambda i, f: 2 * i + 3 * f(i - 1), [0])
        self.assertEqual(seq.get(5), 358)

    def test_func_get_many(self):
        seq = Sequence(lambda i, f: 3 * i + 2 * f(i - 1), [0])
        self.assertEqual(seq.get(3, 5), [33, 78, 171])

