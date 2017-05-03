#!/usr/bin/env python

from cyaron import *
print Geometry.convex_hull(300,fx=lambda x:int(x*1000),fy=lambda x:int(x*1000))
points=Vector.random(300,[1000,1000])
print Geometry.simple_polygon(points)