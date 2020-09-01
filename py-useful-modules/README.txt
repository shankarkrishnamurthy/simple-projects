#
# Description:
#   builds C library, modules
#   tests call C -> python AND python->C
# 
# Types of Calls:
 #   1. c-2-py.c:
 #      Runs as a ELF binary.Loads a custom python module (mult). Call a py fn() in that module. Runs as a ELF binary
 #   2. c-2-py-1.c:
 #      Runs as a ELF binary. Loads py interpreter to run a python fn() ctime/time given as string
 #   3. c-2-py-2.c,c-2py-3.c:
 #      Runs as py program. C .so is loaded as a regular Python module using import. Uses setup.py (distutils) to build
 #   4. py-2-c.py:
 #      Runs Python .py file. ctypes CDLL Loads a .so library built from C. Calls fn() written in C (main.c)
 #

# Read Makefile:

    make
    make test
    make clean
