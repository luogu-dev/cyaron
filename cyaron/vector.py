# coding=utf8

from .utils import *
import random
from enum import IntEnum


class VectorRandomMode(IntEnum):
    unique = 0
    repeatable = 1
    float = 2


class Vector:

    @staticmethod
    def random(num: int = 5, position_range: list = None, mode: VectorRandomMode = 0, **kwargs):
        """
        brief : generating n random vectors in limited space
        param :
            # num            : the number of vectors
            # position_range : a list of limits for each dimension
            #                  single number x represents range (0, x)
            #                  list [x, y] or tuple (x, y) represents range (x, y)
            # mode           : the mode vectors generate, see Enum Class VectorRandomMode
        """
        if position_range is None:
            position_range = [10]

        if num > 1000000:
            raise Exception("num no more than 1e6")
        if not list_like(position_range):
            raise Exception("the 2nd param must be a list or tuple")

        dimension = len(position_range)

        offset = []
        length = []

        vector_space = 1
        for i in range(0, dimension):
            if list_like(position_range[i]):
                if position_range[i][1] < position_range[i][0]:
                    raise Exception("upper-bound should larger than lower-bound")
                offset.append(position_range[i][0])
                length.append(position_range[i][1] - position_range[i][0])
            else:
                offset.append(0)
                length.append(position_range[i])
            vector_space *= (length[i] + 1)

        if mode == VectorRandomMode.unique and num > vector_space:
            raise Exception("1st param is so large that CYaRon can not generate unique vectors")

        result = []
        if mode == VectorRandomMode.repeatable:
            result = [[random.randint(x, y) for x, y in zip(offset, length)] for _ in range(num)]
        elif mode == VectorRandomMode.float:
            result = [[random.uniform(x, y) for x, y in zip(offset, length)] for _ in range(num)]
        elif mode == VectorRandomMode.unique and vector_space > 5 * num:
            # O(NlogN)
            num_set = set()
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
            result = [Vector.get_vector(dimension, length, x) for x in rand_arr[:num]]

            for x in result:
                for i in range(dimension):
                    x[i] += offset[i]

        return result

    @staticmethod
    def get_vector(dimension: int, position_range: list, hashcode: int):
        tmp = []
        for i in range(0, dimension):
            tmp.append(hashcode % (position_range[i] + 1))
            hashcode //= (position_range[i] + 1)
        return tmp
