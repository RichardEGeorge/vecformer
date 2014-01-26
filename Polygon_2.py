import numpy;
import ctypes;

part = ctypes.cdll.LoadLibrary("libpart.dylib");
part.p2_area.restype = ctypes.c_double;
part.quiet_logging();

class Polygon_2(object):

	def __init__(self,name='anon'):
		self.handle = part.p2_create();
		self.name = name;
		if self.handle<0:
			raise Exception('Failed to create a handle for new polygon');
		
	@classmethod
	def as_union(cls,p1,p2):
		p3 = cls('union of %s and %s' % (p1.name,p2.name));
		part.p2_delete(p3.handle);
		p3.handle = part.p2_create_union(p1.handle,p2.handle);
		if p3.handle<0:
			raise Exception('Failed to create a handle for union polygon');

		return p3;

	@classmethod
	def as_intersection(cls,p1,p2):
		p3 = cls('intersection of %s and %s' % (p1.name,p2.name));
		part.p2_delete(p3.handle);
		p3.handle = part.p2_create_intersection(p1.handle,p2.handle);
		if p3.handle<0:
			raise Exception('Failed to create a handle for intersection polygon');

		return p3;

	@classmethod
	def as_difference(cls,p1,p2):
		p3 = cls('difference of %s and %s' % (p1.name,p2.name));
		part.p2_delete(p3.handle);
		p3.handle = part.p2_create_difference(p1.handle,p2.handle);
		if p3.handle<0:
			raise Exception('Failed to create a handle for difference polygon');

		return p3;

	def add_vertex(self,x,y):
		part.p2_add_vertex(ctypes.c_int(self.handle),ctypes.c_double(x),ctypes.c_double(y));

	def define(self,vertices):
		for p in vertices:
			part.p2_add_vertex(ctypes.c_int(self.handle),ctypes.c_double(p[0]),ctypes.c_double(p[1]));

	def __del__(self):
		part.p2_delete(self.handle);

	def vertex_count(self):
		return part.p2_vertex_count(self.handle);

	def area(self):
		return part.p2_area(self.handle);

	def is_simple(self):
		return part.p2_is_simple(self.handle);

	def is_convex(self):
		return part.p2_is_convex(self.handle);

	def get_vertices(self):
		n = self.vertex_count();
		result = numpy.zeros((n,2), dtype = numpy.double);
		state = part.p2_get_vertices(self.handle,ctypes.c_int(2*n),ctypes.c_void_p(result.ctypes.data));
		if state==0:
			return result;

	def is_inside(self,x,y):
		return part.p2_is_inside(self.handle,ctypes.c_double(x),ctypes.c_double(y));



