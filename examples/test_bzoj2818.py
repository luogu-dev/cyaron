#!/usr/bin/env python

from cyaron import *


_n = ati([0,10,1e2,1e3,1e4,1e5,1e6,1e7,1e7,1e7,1e7])

for i in range(1, 11):
    test_data = IO(file_prefix="gcd", data_id=i)
    n = _n[i]
    
    test_data.input_writeln(randint(n//10,n))
    test_data.output_gen("dr.exe")

test_data=1
