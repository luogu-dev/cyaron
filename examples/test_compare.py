#!/usr/bin/env python
from cyaron import *

io = IO()
io.input_write("1111\n")

Compare.program("echo 1111", input=io, std_program="cat")
Compare.program("echo 2", input=io, std_program="cat")

