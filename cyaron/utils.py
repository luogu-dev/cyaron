"""Some utility functions."""
import sys
import random
from typing import cast, Any, Dict, Iterable, Tuple, Union

__all__ = [
    "ati", "list_like", "int_like", "strtolines", "make_unicode",
    "unpack_kwargs", "process_args"
]


def ati(array: Iterable[Any]):
    """Convert all the elements in the array and return them in a list."""
    return [int(i) for i in array]


def list_like(data: Any):
    """Judge whether the object data is like a list or a tuple."""
    return isinstance(data, (tuple, list))


def int_like(data: Any):
    """Judge whether the object data is like a int."""
    return isinstance(data, int)


def strtolines(string: str):
    """
    Split the string by the newline character, remove trailing spaces from each line,
    and remove any blank lines at the end of the the string.
    """
    lines = string.split("\n")
    for i, _ in enumerate(lines):
        lines[i] = lines[i].rstrip()

    while len(lines) > 0 and len(lines[-1]) == 0:
        lines.pop()
    return lines


def make_unicode(data: Any):
    """Convert the data to a string."""
    return str(data)


def unpack_kwargs(
    funcname: str,
    kwargs: Dict[str, Any],
    arg_pattern: Iterable[Union[str, Tuple[str, Any]]],
):
    """Parse the keyword arguments."""
    rv = {}
    kwargs = kwargs.copy()
    for tp in arg_pattern:
        if list_like(tp):
            k, v = cast(Tuple[str, Any], tp)
            rv[k] = kwargs.pop(k, v)
        else:
            tp = cast(str, tp)
            try:
                rv[tp] = kwargs.pop(tp)
            except KeyError:
                raise TypeError(
                    f"{funcname}() missing 1 required keyword-only argument: '{tp}'"
                ) from None
    if kwargs:
        raise TypeError(
            f"{funcname}() got an unexpected keyword argument '{next(iter(kwargs.items()))[0]}'"
        )
    return rv


def process_args():
    """
    Process the command line arguments.
    Now we support:
        - randseed: set the random seed
    """
    for s in sys.argv:
        if s.startswith("--randseed="):
            random.seed(s.split("=")[1])
