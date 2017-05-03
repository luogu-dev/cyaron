import unittest
from cyaron import Polygon,Vector
class TestPolygon(unittest.TestCase):
    def test_convex_hull(self):
        hull = Polygon.convex_hull(300, fx=lambda x:int(x*100000), fy=lambda x:int(x*100000))
        points = hull.points
        points = sorted(points)
        # unique
        tmp = []
        for i in range(0, len(points)):
            if i == 0 or points[i - 1] != points[i]:
                tmp.append(points[i])
        points = tmp
        st = []  # stack
        for i in range(0, len(points)):
            while len(st) >= 2:
                a = st[len(st) - 1]
                b = points[i]
                o = st[len(st) - 2]
                if (a[0] - o[0]) * (b[1] - o[1]) - \
                        (a[1] - o[1]) * (b[0] - o[0]) >= 0:
                    break
                st.pop()
            st.append(points[i])
        g = len(st) + 1
        for i in range(0, len(points) - 1)[::-1]:
            while len(st) >= g:
                a = st[len(st) - 1]
                b = points[i]
                o = st[len(st) - 2]
                if (a[0] - o[0]) * (b[1] - o[1]) - \
                        (a[1] - o[1]) * (b[0] - o[0]) >= 0:
                    break
                st.pop()
            st.append(points[i])
        st.pop()
        self.assertEqual(len(st), len(hull.points))
    def test_perimeter_area(self):
        poly = Polygon([[0,0],[0,1],[1,1],[1,0]])
        self.assertEqual(poly.perimeter(),4)
        self.assertEqual(poly.area(),1)
    def test_simple_polygon(self):
        poly = Polygon.simple_polygon(Vector.random(300, [1000, 1000]))
        points = poly.points
        for i in range(0,len(points)):
            for j in range(i+2,len(points)):
                if j==len(points)-1 and i==0:
                    continue
                a=points[i]
                b=points[(i+1)%len(points)]
                c=points[j]
                d=points[(j+1)%len(points)]
                prod=lambda x,y: x[0]*y[1]-x[1]*y[0]
                t1=prod([c[0]-a[0],c[1]-a[1]],[d[0]-a[0],d[1]-a[1]])\
                  *prod([c[0]-b[0],c[1]-b[1]],[d[0]-b[0],d[1]-b[1]])
                t2=prod([a[0]-c[0],a[1]-c[1]],[b[0]-c[0],b[1]-c[1]])\
                  *prod([a[0]-d[0],a[1]-d[1]],[b[0]-d[0],b[1]-d[1]])
                self.assertFalse(t1<=1e-9 and t2<=1e-9)
