#coding=utf8

from .consts import ALPHABET_SMALL
from .utils import *
import random


class Vector:
    @staticmethod
    def random(num=5, position_range=[10], mode=0, **kwargs):
        # mode 0=unique 1=repeatable 2=float
        if(num > 1000000):
            raise Exception("num no more than 1e6")
        if(not list_like(position_range)):
            raise Exception("the 2nd param must be a list")

        dimension = len(position_range)
        offset = []
        vector_space = 1
        for i in range(0, dimension):
            if(list_like(position_range[i])):
                if(position_range[i][1] < position_range[i][0]):
                    raise Exception("max should larger than min")
                offset.insert(i, position_range[i][0])
                position_range[i] = position_range[i][1] - offset[i]
            else:
                offset.insert(i, 0)
            if(position_range[i] <= 0):
                raise Exception("the difference must more than 0")
            vector_space *= (position_range[i] + 1)
        if(mode == 0 and num > vector_space):
            raise Exception("1st param is too large that CYaRon can not generate unique vectors")
        result = []
        
        if(mode == 2 or mode == 1):
            for i in range(0, num):
                tmp = []
                for j in range(0, dimension):
                    one_num = random.randint(0,position_range[j]) if mode == 1 else random.uniform(0,position_range[j])
                    tmp.insert(j, one_num + offset[j])
                result.insert(i, tmp)
                
        elif((mode == 0 and vector_space > 5 * num)):
            num_set = set([])
            rand = 0;
            for i in range(0, num):
                while True:
                    rand = random.randint(0, vector_space - 1);
                    if(not rand in num_set):
                        break
                # Todo: So how to analyse then complexity? I think it is logn
                num_set.add(rand)
                tmp = Vector.get_vector(dimension, position_range, rand)
                for j in range(0, dimension):
                    tmp[j] += offset[j]
                result.insert(i, tmp)
                         
            
        else:
            # generate 0~vector_space and shuffle
            rand_arr = [i for i in range(0, vector_space)]
            random.shuffle(rand_arr)
            for i in range(0, num):
                tmp = Vector.get_vector(dimension, position_range, rand_arr[i])
                for j in range(0, dimension):
                    tmp[j] += offset[j]
                result.insert(i, tmp)
        return result

    @staticmethod      
    def get_vector(dimension, position_range, hashnum):
        tmp = []
        for i in range(0, dimension):
            tmp.insert(i, hashnum % (position_range[i] + 1))
            hashnum //= (position_range[i] + 1)
        return tmp
        
            
