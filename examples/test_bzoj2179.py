 #!/usr/bin/env python

from cyaron import *


_n = ati([0,10,1e2,5e2,1e3,5e3,1e4,3e4,5e4,6e4,6e4])

for i in range(1, 11):
    test_data = IO(file_prefix="fft", data_id=i)
    n = _n[i]
    
    test_data.input_writeln(n)
    test_data.input_writeln(String.random(n,charset="0123456789"))
    test_data.input_writeln(String.random(n,charset="0123456789"))
    test_data.output_gen("dr.exe")

test_data=1
