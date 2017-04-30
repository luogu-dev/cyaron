#!/usr/bin/env python

from cyaron import *

test_data = IO("heat1.in", "heat1.out")

n = 7
m = 11
s = random.randint(1, n)
t = random.randint(1, n)
test_data.writeln(n, m, s, t)

graph = Graph.graph(n, m, weight_limit=5)
test_data.writeln(graph)

test_data.output_gen("~/Downloads/test")
