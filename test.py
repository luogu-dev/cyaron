#!/usr/bin/env python

from cyaron import io

a = io("test1.in", "test1.out")

a.input_write(1, 2, 3)
a.input_writeln(1, 2, 3, 4)
a.input_write(1, 2, 3)
a.input_writeln(1, 2, 3, 4)
