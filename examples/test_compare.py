#!/usr/bin/env python
from cyaron import *

io = IO()
io.input_write("1\n")

Compare.program("echo 1", input=io, std_program="cat")
Compare.program("echo 2", input=io, std_program="cat")

