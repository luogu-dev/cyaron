from .io import IO
from .graph import Graph, Edge
from random import randint, randrange, uniform, choice, random

"""CYaRon: Yet Another Random Olympic-iNformatics test data generator
By Luogu
This is a tool package for everyone to make the test data quickly.
It has tools for graphs and IO files.
"""

def ati(array):
    """ati(array) -> list
    Convert all the elements in the array and return them in a list.
    """
    return [int(i) for i in array]
