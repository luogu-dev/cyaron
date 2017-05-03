#!/usr/bin/env python
from cyaron import *
print "random convex hull of size 300:"
print Polygon.convex_hull(300, fx=lambda x:int(x*1000), fy=lambda x:int(x*1000))
points = Vector.random(300, [1000, 1000])
print "random simple polygon of size 300:"
print Polygon.simple_polygon(points)