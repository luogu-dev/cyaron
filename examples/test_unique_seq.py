#!/usr/bin/env python

from cyaron import *

_x = ati([0, 5, 10, 20, 100000])
_n = ati([0, 23, 50, 60, 100000])


for i in range(1, 5):
    test_data = IO(file_prefix="test", data_id=i, disable_output=True)
    n = _n[i]
    test_data.input_writeln(n)
    squre = Vector.random(n,[(1,n)])
    for j in range(0,n):
        test_data.input_writeln(squre[j][0])
    # A binary file or shell command that accepts input from stdin and outputs to stdout

