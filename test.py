#!/usr/bin/env python

from cyaron import *

_n = ati([0, 7, 50])
_m = ati([0, 11, 100])

for i in range(1, 3):
    test_data = IO(file_prefix="heat", data_id=i)

    n = _n[i]
    m = _m[i]
    s = randint(1, n)
    t = randint(1, n)
    test_data.input_writeln(n, m, s, t)

    graph = Graph.graph(n, m, weight_limit=5)
    test_data.input_writeln(graph)

    test_data.output_gen("~/Downloads/std_binary")
    # A binary file or shell command that accepts input from stdin and outputs to stdout
