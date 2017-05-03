from .utils import *

class Sequence:
    """Class Sequence: the tool class for sequences.
    """

    def __init__(self, formula, initial_values=()):
        """__init__(self, formula, initial_values=() -> None
            Create a sequence object.
            int formula(int, function) -> the formula function ...
        """
        self.formula = formula
        if list_like(initial_values):
            self.values = dict(enumerate(initial_values))
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
