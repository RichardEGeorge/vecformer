
from Polygon_2 import *;

p1 = Polygon_2("A");

p1.add_vertex(0,0);
p1.add_vertex(10,0);
p1.add_vertex(10,10);
p1.add_vertex(0,10);

p2 = Polygon_2("A");

p2.add_vertex(5,5);
p2.add_vertex(15,5);
p2.add_vertex(15,15);
p2.add_vertex(5,15);

yn = lambda b: "yes" if b else "no";

print "Is polygon simple? %s" % yn(p1.is_simple());
print "Is polygon convex? %s" % yn(p1.is_convex());
print "Polygon %s has signed area : %g" % (p1.name,p1.area());

def test_inside(p,x,y):
	result = p.is_inside(x,y);
	print "Is the point (%g,%g) inside polygon %s? %d" % (x,y,p.name,result);
	return result;

test_inside(p1,5.0,5.0);
test_inside(p1,20.0,20.0);

print p1.get_vertices();

print "union of p1 and p2:"

p3 = Polygon_2.as_union(p1,p2);

print p3.get_vertices();
