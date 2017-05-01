#!/usr/bin/env python

from cyaron import *

test = IO("test.in", "test.out")

test.input_writeln(Sequence(lambda i, f: 2*i+1).get(1))
test.input_writeln(Sequence(lambda i, f: 2*i).get(1, 5))
test.input_writeln(Sequence(lambda i, f: f(i-1)+1, [0]).get(1, 5))
