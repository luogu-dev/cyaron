#!/usr/bin/env python

from cyaron import *


_n = ati([0,10, 100, 500, 1e3, 2e3, 4e3, 5e3, 5e3, 1e4, 1e4])
_m = ati([0,10, 100, 500, 1e3, 2e3, 4e3, 5e3, 1e4, 5e3, 1e4])

for i in range(1, 11):
    test_data = IO(file_prefix="dr", data_id=i)
    print(i,"start")
    n=_n[i]
    m=_m[i]
    
    
    test_data.input_writeln(n,m)
    a=Vector.random(n,[(1,n*n)])
    test_data.input_writeln(a)

    for j in range(0,m):
        arr=Vector.random(1,[(1,n),(1,n),(1,n*n)])
        arr=arr[0]
        
        cz=randint(1,2)
        if cz==1:
            a1=min(arr[0],arr[1])
            a2=max(arr[0],arr[1])
            test_data.input_writeln('Q',a1,a2,randint(1,a2-a1+1))
        else:
            
            test_data.input_writeln('C',arr[0],arr[2])
            


    test_data.output_gen("dr.exe")
    print(i,"end")

test_data=1

