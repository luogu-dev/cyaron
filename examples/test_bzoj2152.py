#!/usr/bin/env python

from cyaron import *

_n = ati([0,10,1e2,5e2,1e3,2e3,3e3,5e3,1e4,2e4,2e4])

for i in range(1, 11):
    test_data = IO(file_prefix="congcong", data_id=i)
    n = _n[i]
    
    t=Graph.tree(n,0.3,0.4,weight_limit=n)
    test_data.input_writeln(n)
    test_data.input_writeln(t)
    
    test_data.output_gen("dr.exe")

test_data=1
