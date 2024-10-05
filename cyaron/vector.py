"""

"""

import random
from enum import IntEnum
from typing import Union, Tuple, List, Set

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

        offset: List[_Number] = []
        length: List[_Number] = []

        vector_space = 1
        for i in range(0, dimension):
            if list_like(position_range[i]):
                if position_range[i][1] < position_range[i][0]:
                    raise ValueError(
                        "upper-bound should be larger than lower-bound")
                offset.append(position_range[i][0])
                length.append(position_range[i][1] - position_range[i][0])
            else:
                offset.append(0)
                length.append(position_range[i])
            vector_space *= (length[i] + 1)

        if mode == VectorRandomMode.unique and num > vector_space:
            raise ValueError(
                "1st param is so large that CYaRon can not generate unique vectors"
            )

        if mode == VectorRandomMode.repeatable:
            result = [[
                random.randint(x, x + y) for x, y in zip(offset, length)
            ] for _ in range(num)]
        elif mode == VectorRandomMode.float:
            result = [[
                random.uniform(x, x + y) for x, y in zip(offset, length)
            ] for _ in range(num)]
        elif mode == VectorRandomMode.unique and vector_space > 5 * num:
            # O(NlogN)
            num_set: Set[int] = set()
            result: List[List[int]] = []
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
    def get_vector(dimension: int, position_range: list, hashcode: int):
        """
        Generates a vector based on the given dimension, position range, and hashcode.
        Args:
            dimension (int): The number of dimensions for the vector.
            position_range (list): A list of integers specifying the range for each dimension.
            hashcode (int): A hashcode used to generate the vector.
        Returns:
            list: A list representing the generated vector.
        """

        tmp: List[int] = []
        for i in range(0, dimension):
            tmp.append(hashcode % (position_range[i] + 1))
            hashcode //= (position_range[i] + 1)
        return tmp
