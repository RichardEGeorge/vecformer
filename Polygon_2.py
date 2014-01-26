import ctypes;

part = ctypes.cdll.LoadLibrary("libpart.dylib");
part.p2_area.restype = ctypes.c_double;
part.quiet_logging();

class Polygon_2(object):

	def __init__(self,name):
		self.handle = part.p2_create();
		self.name = name;

	def add_vertex(self,x,y):
		part.p2_add_vertex(ctypes.c_int(self.handle),ctypes.c_double(x),ctypes.c_double(y));

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

	def is_inside(self,x,y):
		return part.p2_is_inside(self.handle,ctypes.c_double(x),ctypes.c_double(y));



