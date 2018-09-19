all: libpmon.so
	python process.py

libpmon.so: libpmon.c
	gcc -shared -fpic $< -o $@

