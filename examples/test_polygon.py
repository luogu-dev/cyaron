#!/usr/bin/env python
from cyaron import *
print "random convex hull of size 300:"
hull=Polygon.convex_hull(300, fx=lambda x:int(x*1000), fy=lambda x:int(x*1000))
print hull
print "perimeter:"
print hull.perimeter()
print "area:"
print hull.area()
points = Vector.random(300, [1000, 1000])
print "random simple polygon of size 300:"
poly = Polygon.simple_polygon(points)
print poly
print "perimeter:"
print poly.perimeter()
print "area:"
print poly.area()
