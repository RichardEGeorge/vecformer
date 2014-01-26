
from Polygon_2 import *;

p = Polygon_2("A");

p.add_vertex(0,0);
p.add_vertex(0,10);
p.add_vertex(10,10);
p.add_vertex(10,0);

yn = lambda b: "yes" if b else "no";

print "Is polygon simple? %s" % yn(p.is_simple());
print "Is polygon convex? %s" % yn(p.is_convex());
print "Polygon %s has signed area : %g" % (p.name,p.area());

def test_inside(p,x,y):
	result = p.is_inside(x,y);
	print "Is the point (%g,%g) inside polygon %s? %d" % (x,y,p.name,result);
	return result;

test_inside(p,5.0,5.0);
test_inside(p,20.0,20.0);

