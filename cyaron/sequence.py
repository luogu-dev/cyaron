from .utils import *

class Sequence:

    def __init__(self, formula, initial_values=[]):
        self.formula = formula
        if list_like(initial_values):
            self.values = {k: v for (k, v) in enumerate(initial_values)}
        elif isinstance(initial_values, dict):
            self.values = initial_values
        else:
            raise Exception("Initial_values must be either a list/tuple or a dict.")

    def __get_one(self, i):
        if i in self.values:
            return self.values[i]

        self.values[i] = self.formula(i, self.__get_one)
        return self.values[i]

    def get(self, left_range, right_range=None):
        if right_range is None:
            return self.__get_one(left_range)

        return [self.__get_one(i) for i in range(left_range, right_range+1)]
