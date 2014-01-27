#!/usr/bin/env python

from Polygon_2 import *;

p1 = Polygon_2("A");

p1.add_vertex(0,0);
p1.add_vertex(10,0);
p1.add_vertex(10,10);
p1.add_vertex(0,10);

p2 = Polygon_2("B");

p2.add_vertex(5,5);
p2.add_vertex(15,5);
p2.add_vertex(15,15);
p2.add_vertex(5,15);

yn = lambda b: "yes" if b else "no";

def describe_poly(p):
	print "Is polygon %s simple? %s" % (p.name,yn(p.is_simple()));
	print "Is polygon %s convex? %s" % (p.name,yn(p.is_convex()));
	print "Polygon %s has signed area : %g" % (p.name,p.area());
	print "Polygon %s has vertices :\n%s" % (p.name,p.get_vertices());

def test_inside(p,x,y):
	result = p.is_inside(x,y);
	print "Is the point (%g,%g) inside polygon %s? : %s" % (x,y,p.name,yn(result));

describe_poly(p1);

test_inside(p1,4.0,4.0);
test_inside(p1,12.0,12.0);

describe_poly(p2);

test_inside(p2,4.0,4.0);
test_inside(p2,12.0,12.0);

print "union of p1 and p2:"

p3 = Polygon_2.as_union(p1,p2);

describe_poly(p3);

test_inside(p3,4.0,4.0);
test_inside(p3,12.0,12.0);
