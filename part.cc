#include <CGAL/Exact_predicates_exact_constructions_kernel.h>
#include <CGAL/Partition_traits_2.h>
#include <CGAL/partition_2.h>
#include <CGAL/point_generators_2.h>
#include <cassert>
#include <list>
#include <fstream>

typedef CGAL::Exact_predicates_exact_constructions_kernel K;
typedef CGAL::Partition_traits_2<K>                         Traits;
typedef Traits::Point_2                                     Point_2;
typedef Traits::Polygon_2                                   Polygon_2;
typedef Polygon_2::Vertex_iterator                          Vertex_iterator;
typedef std::list<Polygon_2>                                Polygon_list;
typedef CGAL::Creator_uniform_2<int, Point_2>               Creator;

std::map<int,Polygon_2 *> poly2s;
std::map<Polygon_2 *,std::set<Point_2 *> > points;
std::deque<int> p2_handles;

int p2_counter = 1000;

bool verbose = true;

int p2_fresh_handle()
{
	if (p2_handles.size()>0)
	{
		int result = p2_handles.front();
		p2_handles.pop_front();
		return result;
	}
	return p2_counter++;
}

extern "C" void verbose_logging()
{
	verbose = true;
}

extern "C" void quiet_logging()
{
	verbose = false;
}

extern "C" int p2_create()
{
	Polygon_2 *p = new Polygon_2();
	int fresh_handle = p2_fresh_handle();

	if (verbose) std::cout << "C++: New polygon at " << p << " with handle " << fresh_handle << std::endl;
 
	poly2s[fresh_handle]=p;
	return fresh_handle;
}

extern "C" int p2_delete(int k)
{
	if (poly2s.find(k)!=poly2s.end())
	{
		Polygon_2 *p = poly2s[k];
		// Also erase points associated with the polygon
		std::set<Point_2 *>::iterator it;
		for (it=points[p].begin();it!=points[p].end();it++) delete (*it);
		points.erase(p);
		// Free the polygon
		poly2s.erase(k);
		p2_handles.push_back(k);
		delete p;
		return 0;
	}
	else
	{
		return -1;
	}
}

extern "C" int p2_add_vertex(int k,double x,double y)
{
	if (verbose) std::cout << "C++: adding point (" << x << "," << y << ") to polygon " << k << std::endl;

	if (poly2s.find(k)!=poly2s.end())
	{
		Polygon_2 *p = poly2s[k];
		Point_2 *pt = new Point_2(x,y);
		points[p].insert(pt);
		p->push_back(*pt);
		return 0;
	}
	else
	{
		return -1;
	}	
}

extern "C" int p2_is_simple(int k)
{
	if (poly2s.find(k)!=poly2s.end())
	{
		Polygon_2 *p = poly2s[k];
		return (p->is_simple()) ? 1 : 0;
	}
	else
	{
		return -1;
	}	
}

extern "C" int p2_vertex_count(int k)
{
	if (poly2s.find(k)!=poly2s.end())
	{
		Polygon_2 *p = poly2s[k];
		int result = p->size();
		if (verbose) std::cout << "C++: polygon " << k << " has " << result << " vertices" << std::endl;
		return result;
	}
	else
	{
		return -1;
	}	
}

extern "C" double p2_area(int k)
{
	if (poly2s.find(k)!=poly2s.end())
	{
		Polygon_2 *p = poly2s[k];
		double result = CGAL::to_double(p->area());
		if (verbose) std::cout << "C++: Polygon " << k << " has area " << result << std::endl;
		return result;
	}
	else
	{
		return 0.0;
	}	
}

extern "C" int p2_is_convex(int k)
{
	if (poly2s.find(k)!=poly2s.end())
	{
		Polygon_2 *p = poly2s[k];
		bool result = p->is_convex();
		if (verbose) std::cout << "C++: Polygon " << k << " is convex: " << result << std::endl;
		return (result) ? 1 : 0;
	}
	else
	{
		return -1;
	}	
}

extern "C" int p2_is_inside(int k,double x,double y)
{
	Traits       traits;

	if (poly2s.find(k)!=poly2s.end())
	{
		Polygon_2 *p = poly2s[k];
		if (verbose) std::cout << "C++: testing if point (" << x << "," << y << ") is in polygon " << k << std::endl;

		switch(CGAL::bounded_side_2(p->vertices_begin(), p->vertices_end(),Point_2(x,y), traits))
		{
    			case CGAL::ON_BOUNDED_SIDE:
			return 1;
    			case CGAL::ON_BOUNDARY:
			return 2;
		        case CGAL::ON_UNBOUNDED_SIDE:
			return 0;
		}
		return -2;
	}
	else
	{
		return -1;
        }
}
