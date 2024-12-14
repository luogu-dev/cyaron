"""
This module provides a `RangeQuery` class for generating queries
based on limits of each dimension.

Classes:
    RangeQuery: A class for generating random queries.
    
Usage:
    n = randint(1, 10)
    q = randint(1, 10)
    Q = Query.random(q, [(1, n)])
"""

import random
from enum import IntEnum
from typing import Optional, Union, Tuple, List

from .utils import list_like


class RangeQueryRandomMode(IntEnum):
    less = 0  # disallow l = r
    allow_equal = 1  # allow l = r


class RangeQuery:
    """A class for generating random queries."""

    @staticmethod
    def random(
        num: int = 1,
        position_range: Optional[List[Union[int, Tuple[int, int]]]] = None,
        mode: RangeQueryRandomMode = RangeQueryRandomMode.allow_equal,
    ) -> List[Tuple[List[int], List[int]]]:
        """
        Generate `num` random queries with dimension limit.
        Args:
            num: the number of queries
            position_range: a list of limits for each dimension
                single number x represents range [1, x]
                list [x, y] or tuple (x, y) represents range [x, y]
            mode: the mode queries generate, see Enum Class RangeQueryRandomMode
        """
        if position_range is None:
            position_range = [10]

        if not list_like(position_range):
            raise TypeError("the 2nd param must be a list or tuple")

        result: List[Tuple[List[int], List[int]]] = []
        for _ in range(num):
            result.append(RangeQuery.get_one_query(position_range, mode))
        return result

    @staticmethod
    def get_one_query(
        position_range: Optional[List[Union[int, Tuple[int, int]]]] = None,
        mode: RangeQueryRandomMode = RangeQueryRandomMode.allow_equal,
    ) -> Tuple[List[int], List[int]]:
        dimension = len(position_range)
        query_l: List[int] = []
        query_r: List[int] = []
        for i in range(dimension):
            cur_range: Tuple[int, int]
            if isinstance(position_range[i], int):
                cur_range = (1, position_range[i])
            elif len(position_range[i]) == 1:
                cur_range = (1, position_range[i][0])
            else:
                cur_range = position_range[i]

            if cur_range[0] > cur_range[1]:
                raise ValueError("upper-bound should be larger than lower-bound")
            if mode == RangeQueryRandomMode.less and cur_range[0] == cur_range[1]:
                raise ValueError(
                    "mode is set to less but upper-bound is equal to lower-bound"
                )

            l = random.randint(cur_range[0], cur_range[1])
            r = random.randint(cur_range[0], cur_range[1])
            # Expected complexity is O(log(1 / V))
            while mode == RangeQueryRandomMode.less and l == r:
                l = random.randint(cur_range[0], cur_range[1])
                r = random.randint(cur_range[0], cur_range[1])
            if l > r:
                l, r = r, l
            query_l.append(l)
            query_r.append(r)
        return (query_l, query_r)
