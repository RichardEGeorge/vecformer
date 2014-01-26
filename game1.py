#!/usr/bin/env python

import os;
import sys;
import xml.etree.ElementTree as ElementTree;
from math import *; 
import random;

# Dependencies: triangle, pyglet

import triangle;

# Patch a bug in Canopy
if sys.platform=='darwin':
	os.environ['DYLD_FALLBACK_LIBRARY_PATH'] = '/lib:/usr/lib:/usr/local/lib:' + os.environ['DYLD_FALLBACK_LIBRARY_PATH'];

import pyglet;

# So ugly - this will go in the __init__ method of a class one day

global world_x,world_y,velocity_x,velocity_y,acceleration_x,acceleration_y,active_acceleration;
global ww,hh;

world_x = 0.0;
world_y = 0.0;
velocity_x = 0.0;
velocity_y = 0.0;
acceleration_x = 0.0;
acceleration_y = 0.0;
max_velocity = 300.0;
drag = 0.25; # Time for velocity to fall to 1/e
tt = 0.0;
active_acceleration = max_velocity/drag;

# Why yes, I will hard code the window size

ww = 800.0;
hh = 600.0;

circular_list = lambda m: [[n,(n+1) % m] for n in range(0,m)]; # Make a list of vertices running round the edge of a polygon
noisy = lambda c: min(255,max(0,c+random.randrange(-32,32))); # Add a bit of noise to the colours of an object

def parse_coords(pts): 
	'''Parse an SVG path:d attribute into a list of coordinates'''
	for p in pts:
		if p=='z':
			raise StopIteration
		coords = p.split(',');
		yield list((float(coords[0]),-float(coords[1])));
			
# The windowing code starts here

window = pyglet.window.Window(int(ww),int(hh));
keyboard = pyglet.window.key.KeyStateHandler();
window.push_handlers(keyboard);

# Compile a list of OpenGL operations into a batch

batch = pyglet.graphics.Batch();

# Some demo openGL commands

#batch.add(1,pyglet.gl.GL_POINTS,None,('v2i',(0,0)),('c3B',(255,0,255)));
#batch.add_indexed(4,pyglet.gl.GL_TRIANGLES,None,[0,1,2,0,2,3], \
#	('v2i',(100,100,100,200,200,200,200,100)),('c3B',(255,0,255,0,255,255,255,255,0,255,255,255)));

# Read the level file

tree = ElementTree.parse('level4.svg');

root = tree.getroot();

for group in root.findall('{http://www.w3.org/2000/svg}g'):
	# Find each layer in the SVG file

	for item in group.findall('{http://www.w3.org/2000/svg}path'):
		# Find each polygon outline

		# item.attrib["d"] contains a list like "M 100,100 100,200 200,200 200,100 z" which defines the coordinates of the outline of the polygon

		# Parse such a specification into a list of coordinates
		points = item.attrib["d"].split(" ");
		pts = list(parse_coords(points[1:]));
		
		# OpenGL expects an array of triangles to plot. 'segments' lists the outline of the polygon, and 'vertices' lists the coordinates
		process = triangle.triangulate({'segments':circular_list(len(pts)), 'vertices':pts},'p');

		# Unpack the data and assemble it in the format OpenGL expects
		triangle_count = len(process['triangles']);
		independent_vertex_count = len(process['vertices']);
		vertex_coords = [point for sublist in process['vertices'] for point in sublist];
		vertex_indices = [vertex for sublist in process['triangles'] for vertex in sublist];
		colours = [noisy(i) for dummy in process['vertices'] for i in [128,255,128]];
	
		# Some debugging info
 
		print 'input points = %s' % pts;
		print 'vertex_coords=%s, len(vertex_coords)=%d' % (vertex_coords,len(vertex_coords))
		print 'vertex_indices=%s, len(vertex_indices)=%d' % (vertex_indices,len(vertex_indices))
		print 'triangle count = %d' % triangle_count;
		print 'independent vertex count = %d' % independent_vertex_count;
		print 'colours = %s' % colours

		batch.add_indexed(independent_vertex_count,pyglet.gl.GL_TRIANGLES,None,tuple(vertex_indices), \
			('v2f',tuple(vertex_coords)),('c3B',tuple(colours)));
	

# The drawing routine

@window.event
def on_draw():
	global ww,hh;
	# Blank window
	window.clear();

	# Move the viewport
	pyglet.gl.glMatrixMode(pyglet.gl.GL_PROJECTION);
	pyglet.gl.glLoadIdentity();
	pyglet.gl.glOrtho(-ww/2.0, ww/2.0, -hh*.9, hh*.1, -1, 1);
	pyglet.gl.glTranslatef(-world_x,-world_y,0,0);
	pyglet.gl.glRotatef(3.0*sin(2.0*pi*tt/8.0),0.0,0.0,1.0);
	pyglet.gl.glScalef(0.25,0.25,1.0);
	
	pyglet.gl.glMatrixMode(pyglet.gl.GL_MODELVIEW);
	pyglet.gl.glLoadIdentity();

	batch.draw();
	
def update(dt):
	'''Add acceleration to velocity, add velocity to position, update acceleration according to keypressed, press space to jump and arrow keys to move'''

	global world_x,world_y,velocity_x,velocity_y,acceleration_x,acceleration_y,active_acceleration,tt;

	tt+= dt;
	world_x += velocity_x * dt;
	world_y += velocity_y * dt;

	acceleration_x = 0.0;
	acceleration_y = 0.0;
	
	if world_y > 0:
		acceleration_y = -600.0;
		friction = 0.1;
	else:
		acceleration_y = 0.0;
		world_y = 0.0;
		velocity_y = 0.0;
		friction = 1.0;
		
		if keyboard[pyglet.window.key.SPACE]: 
			velocity_y = 400.0;
			
	if keyboard[pyglet.window.key.RIGHT]: 
		acceleration_x = active_acceleration*friction;
	if keyboard[pyglet.window.key.LEFT]: 
		acceleration_x = -active_acceleration*friction;

	velocity_x += acceleration_x * dt;
	velocity_y += acceleration_y * dt;
	
	if world_y <= 0:
		velocity_x *= exp(-dt/drag);
		velocity_y *= exp(-dt/drag);
	
pyglet.clock.schedule_interval(update,1.0/30.0);
	
# window.push_handlers(pyglet.window.event.WindowEventLogger())

pyglet.app.run();
