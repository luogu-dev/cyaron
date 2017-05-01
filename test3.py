#!/usr/bin/env python

from cyaron import *
import random

_n = ati([0, 7, 8])

def oper(x):
    return "%d %d  weight=%d,%d" % (x.start, x.end, x.weight[0], x.weight[1])

def wg():
    return [random.randint(3, 5), random.randint(1, 10)]

for i in range(1, 3):
    test_data = IO(file_prefix="test", data_id=i)
    n = _n[i]
    test_data.input_writeln(n)
    graph = Graph.hack_spfa(n, weight_gen=wg)
    test_data.input_writeln(graph.to_str(output=oper))
    test_data.input_writeln('============Shuffle============')
    test_data.input_writeln(graph.to_str(output=oper, shuffle=True))
    test_data.output_gen("~/Downloads/std_binary")
    # A binary file or shell command that accepts input from stdin and outputs to stdout
