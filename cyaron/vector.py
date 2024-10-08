"""

"""

import random
from enum import IntEnum
from typing import Sequence, Union, Tuple, List, Set
from typing import cast as typecast

from .utils import list_like


class VectorRandomMode(IntEnum):
    unique = 0
    repeatable = 1
    float = 2


_Number = Union[int, float]


class Vector:
    """A class for generating random vectors"""

    IntVector = List[List[int]]
    FloatVector = List[List[float]]

    @staticmethod
    def random(
        num: int = 5,
        position_range: Union[List[Union[_Number, Tuple[_Number, _Number]]],
                              None] = None,
        mode: VectorRandomMode = VectorRandomMode.unique,
    ) -> Union[IntVector, FloatVector]:
        """
        Generate `num` random vectors in limited space
        Args:
            num: the number of vectors
            position_range: a list of limits for each dimension
                single number x represents range (0, x)
                list [x, y] or tuple (x, y) represents range (x, y)
            mode: the mode vectors generate, see Enum Class VectorRandomMode
        """
        if position_range is None:
            position_range = [10]

        if not list_like(position_range):
            raise TypeError("the 2nd param must be a list or tuple")

        dimension = len(position_range)

        offset: Sequence[_Number] = []
        length: Sequence[_Number] = []

        vector_space = 1
        for i in range(0, dimension):
            now_position_range = position_range[i]
            if isinstance(now_position_range, tuple):
                if now_position_range[1] < now_position_range[0]:
                    raise ValueError(
                        "upper-bound should be larger than lower-bound")
                offset.append(now_position_range[0])
                length.append(now_position_range[1] - now_position_range[0])
            else:
                offset.append(0)
                length.append(now_position_range)
            vector_space *= (length[i] + 1)

        if mode == VectorRandomMode.unique and num > vector_space:
            raise ValueError(
                "1st param is so large that CYaRon can not generate unique vectors"
            )

        result: Union[List[List[int]], List[List[float]]]
        if mode == VectorRandomMode.repeatable:
            offset = typecast(Sequence[int], offset)
            length = typecast(Sequence[int], length)
            result = [[
                random.randint(x, x + y) for x, y in zip(offset, length)
            ] for _ in range(num)]
        elif mode == VectorRandomMode.float:
            result = [[
                random.uniform(x, x + y) for x, y in zip(offset, length)
            ] for _ in range(num)]
        elif mode == VectorRandomMode.unique and vector_space > 5 * num:
            # O(NlogN)
            offset = typecast(Sequence[int], offset)
            length = typecast(Sequence[int], length)
            vector_space = typecast(int, vector_space)
            num_set: Set[int] = set()
            result = typecast(List[List[int]], [])
            for i in range(0, num):
                while True:
                    rand = random.randint(0, vector_space - 1)
                    if rand not in num_set:
                        break
                num_set.add(rand)
                tmp = Vector.get_vector(dimension, length, rand)
                for j in range(0, dimension):
                    tmp[j] += offset[j]
                result.append(tmp)
        else:
            # generate 0~vector_space and shuffle
            offset = typecast(Sequence[int], offset)
            length = typecast(Sequence[int], length)
            vector_space = typecast(int, vector_space)
            rand_arr = list(range(0, vector_space))
            random.shuffle(rand_arr)
            result = [
                Vector.get_vector(dimension, length, x) for x in rand_arr[:num]
            ]

            for x in result:
                for i in range(dimension):
                    x[i] += offset[i]

        return result

    @staticmethod
    def get_vector(dimension: int, position_range: Sequence[int],
                   hashcode: int):
        """
        Generates a vector based on the given dimension, position range, and hashcode.
        Args:
            dimension: The number of dimensions for the vector.
            position_range: A list of integers specifying the range for each dimension.
            hashcode: A hashcode used to generate the vector.
        Returns:
            list: A list representing the generated vector.
        """

        tmp: List[int] = []
        for i in range(0, dimension):
            tmp.append(hashcode % (position_range[i] + 1))
            hashcode //= (position_range[i] + 1)
        return tmp
