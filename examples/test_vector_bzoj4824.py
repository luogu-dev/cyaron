#!/usr/bin/env python

from cyaron import *


_n = ati([0,10,18,20,25,30,80,100,100,100,100])

for i in range(1, 11):
    test_data = IO(file_prefix="keyborad", data_id=i)
    n = _n[i]
    ostr = String.random(n,charset="<>")
    if i==7:
        ostr = '<'*n
    if i==8:
        ostr='<'*(n-1)+'>'
    test_data.input_writeln(n,ostr)


    test_data.output_gen("a.exe")

test_data=1
