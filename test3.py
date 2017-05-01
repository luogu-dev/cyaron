#!/usr/bin/env python

from cyaron import *

_n = ati([0, 7, 8])

def oper(x):
  return "%d %d  weight=%d" % (x.start, x.end, x.weight)

for i in range(1, 3):
    test_data = IO(file_prefix="test", data_id=i)
    n = _n[i]
    test_data.writeln(n)
    graph = Graph.hack_spfa(n,weight_limit=(1,5))
    test_data.writeln(graph.to_str(output=oper))
    test_data.writeln('============Shuffle============')
    test_data.writeln(graph.to_str(output=oper,shuffle=True))
    test_data.output_gen("~/Downloads/std_binary")
    # A binary file or shell command that accepts input from stdin and outputs to stdout
