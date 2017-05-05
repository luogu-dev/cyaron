#!/usr/bin/env python

from cyaron import *

_n = ati([0, 7, 50])

def oper(x):
    return "%d %d" % (x.start, x.end)

for i in range(1, 3):
    test_data = IO(file_prefix="test", data_id=i)
    n = _n[i]
    test_data.input_writeln(n)
    graph = Graph.tree(n, 0.3, 0.3)
    test_data.input_writeln(graph.to_str(output=oper))
    test_data.input_writeln('============Shuffle============')
    test_data.input_writeln(graph.to_str(output=oper, shuffle=True))
    test_data.output_gen("~/Downloads/std_binary")
    # A binary file or shell command that accepts input from stdin and outputs to stdout
