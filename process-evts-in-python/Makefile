all: libpmon.so
	python monitor-fork-exec.py

libpmon.so: libpmon.c
	gcc -shared -fpic $< -o $@

