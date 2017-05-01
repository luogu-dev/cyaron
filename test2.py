#!/usr/bin/env python

from cyaron import *

_n = ati([0, 7, 50])
_m = ati([0, 11, 100])

def oper(x):
  return "%d %d" % (x.start, x.end)

for i in range(1, 3):
    test_data = IO(file_prefix="test", data_id=i)
    n = _n[i]
    m = _m[i]
    s = randint(1, n)
    t = randint(1, n)
    test_data.writeln(n, m, s, t)
    graph = Graph.tree(n,0.3,0.3)
    test_data.writeln(graph.to_str(output=oper))
    test_data.writeln('============Shuffle============')
    test_data.writeln(graph.to_str(output=oper,shuffle=True))
    test_data.output_gen("~/Downloads/std_binary")
    # A binary file or shell command that accepts input from stdin and outputs to stdout
