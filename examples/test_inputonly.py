#!/usr/bin/env python

from cyaron import *

test = IO("test.in")
for i in range(5):
    test.input_writeln(
        Sequence(lambda i, f: i-1).get(1, 10),
        separator=","
    )