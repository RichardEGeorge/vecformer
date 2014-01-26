all: libpart.dylib test_poly.txt

test_poly.txt: test_poly.py libpart.dylib Polygon_2.py
	python test_poly.py | tee test_poly.txt

libpart.dylib: part.cc
	g++ part.cc -I/opt/local/include -L/opt/local/lib -dynamiclib -o libpart.dylib -lCGAL -lgmp -lmpfr -lboost_thread-mt

clean:
	rm -f libpart.dylib 

