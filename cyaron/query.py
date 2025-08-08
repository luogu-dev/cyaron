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
    result: List[Tuple[List[int], List[int], List]]  # Vector L, R, weights.

    def __init__(self):
        self.result = []

    def __len__(self):
        return len(self.result)

    def __getitem__(self, item):
        return self.result[item]

    def __str__(self):
        """__str__(self) -> str
            Return a string to output the queries. 
            The string contains all the queries with l and r in a row, splits with "\\n".
        """
        return self.to_str()

    def to_str(self):
        """
        Return a string to output the queries. 
        The string contains all the queries with l and r (and w if generated) in a row, splits with "\\n".
        """
        res = ''
        for l, r, w in self.result:
            l_to_str = [str(x) for x in l]
            r_to_str = [str(x) for x in r]
            w_to_str = [str(x) for x in w]
            res += ' '.join(l_to_str) + ' ' + ' '.join(r_to_str)
            if len(w_to_str) > 0:
                res += ' ' + ' '.join(w_to_str)
            res += '\n'
        return res[:-1]  # remove the last '\n'

    @staticmethod
    def random(
        num: int = 1,
        position_range: Optional[List[Union[int, Tuple[int, int]]]] = None,
        mode: RangeQueryRandomMode = RangeQueryRandomMode.allow_equal,
        weight_generator=None,
        big_query: float = 0.2,
    ):
        """
        Generate `num` random queries with dimension limit.
        Args:
            num: the number of queries
            position_range: a list of limits for each dimension
                single number x represents range [1, x]
                list [x, y] or tuple (x, y) represents range [x, y]
            mode: the mode queries generate, see Enum Class RangeQueryRandomMode
            weight_generator: A function that generates the weights for the queries. It should:
                - Take the index of query (starting from 1), starting and ending positions as input.
                - Return a list of weights of any length.
            big_query: a float number representing the probability for generating big queries.
        """
        if position_range is None:
            position_range = [10]

        if weight_generator is None:
            weight_generator = lambda i, l, r: []

        ret = RangeQuery()

        if not list_like(position_range):
            raise TypeError("the 2nd param must be a list or tuple")

        for i in range(num):
            ret.result.append(
                RangeQuery.get_one_query(position_range, big_query, mode,
                                         weight_generator, i + 1))
        return ret

    @staticmethod
    def get_one_query(
            position_range: Optional[List[Union[int, Tuple[int, int]]]] = None,
            big_query: float = 0.2,
            mode: RangeQueryRandomMode = RangeQueryRandomMode.allow_equal,
            weight_generator=None,
            index: int = 1) -> Tuple[List[int], List[int], List]:
        """
        Generate a pair of query lists (query_l, query_r, w) based on the given position ranges and mode.
        Args:
            position_range (Optional[List[Union[int, Tuple[int, int]]]]): A list of position ranges. Each element can be:
                - An integer, which will be treated as a range from 1 to that integer.
                - A tuple of two integers, representing the lower and upper bounds of the range.
            mode (RangeQueryRandomMode): The mode for generating the queries. It can be:
                - RangeQueryRandomMode.allow_equal: Allow the generated l and r to be equal.
                - RangeQueryRandomMode.less: Ensure that l and r are not equal.
            weight_generator: A function that generates the weights for the queries. It should:
                - Take the index of query (starting from 1), starting and ending positions as input.
                - Return a list of weights of any length.
        Returns:
            Tuple[List[int], List[int]]: A tuple containing two lists:
                - query_l: A list of starting positions.
                - query_r: A list of ending positions.
        Raises:
            ValueError: If the upper-bound is smaller than the lower-bound.
            ValueError: If the mode is set to less but the upper-bound is equal to the lower-bound.
        """
        if position_range is None:
            position_range = [10]

        if weight_generator is None:
            weight_generator = lambda i, l, r: []

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
                raise ValueError(
                    "upper-bound should be larger than lower-bound")
            if mode == RangeQueryRandomMode.less and cur_range[0] == cur_range[
                    1]:
                raise ValueError(
                    "mode is set to less but upper-bound is equal to lower-bound"
                )

            if random.random() < big_query:
                # Generate a big query
                cur_l = cur_range[1] - cur_range[0] + 1
                lb = max(
                    2, cur_l //
                    2) if mode == RangeQueryRandomMode.less else cur_l // 2
                ql = random.randint(lb, cur_l)
                l = random.randint(cur_range[0], cur_range[1] - ql + 1)
                r = l + ql - 1
            else:
                l = random.randint(cur_range[0], cur_range[1])
                r = random.randint(cur_range[0], cur_range[1])
                # Expected complexity is O(1)
                # We can use random.sample, But it's actually slower according to benchmarks.
                while mode == RangeQueryRandomMode.less and l == r:
                    l = random.randint(cur_range[0], cur_range[1])
                    r = random.randint(cur_range[0], cur_range[1])
                if l > r:
                    l, r = r, l

            query_l.append(l)
            query_r.append(r)
        return (query_l, query_r, weight_generator(index, query_l, query_r))
