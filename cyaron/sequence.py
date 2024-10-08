"""
This module provides a `Sequence` class for generating sequences
based on a given formula and initial values.

Classes:
    Sequence: A class for creating and managing sequences.
"""

from typing import Callable, Dict, List, Optional, Tuple, TypeVar, Union
from typing import cast as typecast

from .utils import list_like

T = TypeVar('T')


class Sequence:
    """A class for creating and managing sequences."""

    def __init__(self,
                 formula: Callable[[int, Callable[[int], T]], T],
                 initial_values: Union[List[T], Tuple[T, ...], Dict[int,
                                                                    T]] = ()):
        """
        Initialize a sequence object.
        Parameters:
            formula: A function that defines the formula for the sequence.
            initial_values (optional): Initial values for the sequence. 
                Can be a list, tuple, or dictionary. Defaults to an empty tuple.
        """
        if not callable(formula):
            raise TypeError("formula must be a function")
        self.formula = formula
        if list_like(initial_values):
            self.values = dict(
                enumerate(
                    typecast(Union[List[T], Tuple[T, ...]], initial_values)))
        elif isinstance(initial_values, dict):
            self.values = initial_values
        else:
            raise TypeError(
                "Initial_values must be either a list/tuple or a dict.")

    def get_one(self, i: int):
        """
        Retrieve the value at the specified index, computing it if necessary.
        Args:
            i (int): The index of the value to retrieve.
        Returns:
            The value at the specified index.
        If the value at the specified index is not already computed, it will be
        calculated using the provided formula and stored for future access.
        """
        if i in self.values:
            return self.values[i]
        self.values[i] = self.formula(i, self.get_one)
        return self.values[i]

    def get(self, left_range: int, right_range: Optional[int] = None):
        """
        Retrieve a sequence of elements within the specified range.
        If only `left_range` is provided, a single element is retrieved.
        If both `left_range` and `right_range` are provided, a list of elements
        from `left_range` to `right_range` (inclusive) is retrieved.
        Args:
            left_range: The starting index or the single index to retrieve.
            right_range (optional): The ending index for the range retrieval. Defaults to None.
        Returns:
            A single element if `right_range` is None, otherwise a list of elements.
        """
        if right_range is None:
            return self.get_one(left_range)
        return [self.get_one(i) for i in range(left_range, right_range + 1)]
