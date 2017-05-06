#!/usr/bin/env python

from cyaron import *


_n = ati([0, 10, 99, 100, 500, 1e3, 5e3, 3e4, 6e4, 9e4, 1e5])
_r = ati([0, 10, 20, 50,  2e2, 2e2, 4e2, 4e2, 7e2, 3e3, 4e3])
_c = ati([0, 10, 20, 50,  2e2, 3e2, 1e3, 5e2, 5e3, 3e3, 5e3])

def oper(x):
    return "%d %d" % (x,start, x,end)

for i in range(1, 11):
    test_data = IO(file_prefix="sqare", data_id=i)
    n = _n[i]
    r = _r[i]
    c = _c[i]
    
    test_data.input_writeln(r,c,n)
    squre = Vector.random(n,[(1,int(math.sqrt(n)+100)),(1,int(math.sqrt(n)+100))])
    for j in range(0,n):
        test_data.input_writeln(squre[j][0], squre[j][1], randint(1,c))
    test_data.output_gen("a.exe")

test_data=1
