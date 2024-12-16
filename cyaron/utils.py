import sys
import random
from typing import List, Optional, cast, Any, Dict, Iterable, Tuple, Union

__all__ = [
    "ati",
    "list_like",
    "int_like",
    "strtolines",
    "make_unicode",
    "unpack_kwargs",
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
    for i in range(len(lines)):
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
                )
    if kwargs:
        raise TypeError(
            f"{funcname}() got an unexpected keyword argument '{next(iter(kwargs.items()))[0]}'"
        )
    return rv


def get_seed_from_argv(argv: Optional[List[str]] = None):
    """
    Calculate a random seed from the command-line arguments,
    referencing the implementation of `testlib.h`, but with differing behavior.

    https://github.com/MikeMirzayanov/testlib/blob/9ecb11126c16caeda2ba375e0084b3ddd03d4ace/testlib.h#L800
    """
    seed = 3905348978240129619
    for s in sys.argv[1:] if argv is None else argv:
        for c in s:
            seed = seed * 0x5DEECE66D + ord(c) + 0xB
            seed &= 0xFFFFFFFFFFFF
        seed += 0x88A12C38
    return seed & 0xFFFFFFFFFFFF


def set_seed_from_argv(argv: Optional[List[str]] = None, version: int = 2):
    """Set the random seed from the command-line arguments."""
    random.seed(get_seed_from_argv(argv), version)
