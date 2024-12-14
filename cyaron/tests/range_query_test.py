import unittest
import random
from cyaron.query import *
from cyaron.vector import *


def valid_query(l, r, mode: RangeQueryRandomMode, limits) -> bool:
    if len(l) != len(r) or len(l) != len(limits):
        return False
    dimension = len(l)
    for i in range(dimension):
        cur_limit = limits[i]
        if isinstance(cur_limit, int):
            cur_limit = (1, cur_limit)
        elif len(limits[i]) == 1:
            cur_limit = (1, cur_limit[0])
        if l[i] > r[i] or (l[i] == r[i] and mode == RangeQueryRandomMode.less):
            print("bound", l[i], r[i])
            return False
        if not (cur_limit[0] <= l[i] <= r[i] <= cur_limit[1]):
            print("limit", cur_limit[0], cur_limit[1], l[i], r[i])
            return False
    return True


class TestRangeQuery(unittest.TestCase):
    def test_allow_equal_v1(self):
        dimension = random.randint(1, 10)
        limits = Vector.random(dimension, [1000])  # n1, n2 ...
        Q = RangeQuery.random(10**5, limits)
        self.assertEqual(len(Q), 10**5)
        for i in range(10**5):
            self.assertTrue(
                valid_query(Q[i][0], Q[i][1], RangeQueryRandomMode.allow_equal, limits)
            )

    def test_allow_equal_v2_throw(self):
        dimension = random.randint(1, 10)
        limits = Vector.random(dimension, [1000, 1000])  # n1, n2 ...
        conflict = False
        for i in range(dimension):
            conflict = conflict or limits[i][0] > limits[i][1]
        throw = False
        try:
            Q = RangeQuery.random(10**5, limits)
            self.assertEqual(len(Q), 10**5)
            for i in range(10**5):
                self.assertTrue(
                    valid_query(
                        Q[i][0], Q[i][1], RangeQueryRandomMode.allow_equal, limits
                    )
                )
        except:
            throw = True

        self.assertEqual(throw, conflict)

    def test_allow_equal_v2_no_throw(self):
        dimension = random.randint(1, 10)
        limits = Vector.random(dimension, [1000, 1000])  # n1, n2 ...
        for i in range(dimension):
            if limits[i][0] > limits[i][1]:
                limits[i][0], limits[i][1] = limits[i][1], limits[i][0]
        Q = RangeQuery.random(10**5, limits)
        self.assertEqual(len(Q), 10**5)
        for i in range(10**5):
            self.assertTrue(
                valid_query(Q[i][0], Q[i][1], RangeQueryRandomMode.allow_equal, limits)
            )

    def test_less_v1(self):
        dimension = random.randint(1, 10)
        limits = Vector.random(dimension, [1000])  # n1, n2 ...
        Q = RangeQuery.random(10**5, limits, RangeQueryRandomMode.less)
        self.assertEqual(len(Q), 10**5)
        for i in range(10**5):
            self.assertTrue(
                valid_query(Q[i][0], Q[i][1], RangeQueryRandomMode.less, limits)
            )

    def test_less_v2_throw(self):
        dimension = random.randint(1, 10)
        limits = Vector.random(dimension, [1000, 1000])  # n1, n2 ...
        conflict = False
        for i in range(dimension):
            conflict = conflict or limits[i][0] >= limits[i][1]
        throw = False
        try:
            Q = RangeQuery.random(10**5, limits, RangeQueryRandomMode.less)
            self.assertEqual(len(Q), 10**5)
            for i in range(10**5):
                self.assertTrue(
                    valid_query(Q[i][0], Q[i][1], RangeQueryRandomMode.less, limits)
                )
        except:
            throw = True

        self.assertEqual(throw, conflict)

    def test_less_v2_no_throw(self):
        dimension = random.randint(1, 10)
        limits = Vector.random(dimension, [1000, 1000])  # n1, n2 ...
        for i in range(dimension):
            while limits[i][0] == limits[i][1]:
                limits[i][0] = random.randint(1, 1000)
                limits[i][1] = random.randint(1, 1000)
            if limits[i][0] > limits[i][1]:
                limits[i][0], limits[i][1] = limits[i][1], limits[i][0]
        Q = RangeQuery.random(10**5, limits, RangeQueryRandomMode.less)
        self.assertEqual(len(Q), 10**5)
        for i in range(10**5):
            self.assertTrue(
                valid_query(Q[i][0], Q[i][1], RangeQueryRandomMode.less, limits)
            )
