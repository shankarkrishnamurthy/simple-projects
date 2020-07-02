#
# Description:
#   builds C library, modules
#   tests call C -> python AND python->C
# 
# Types of Calls:
 #   1. c-2-py.c:
 #      Loads a custom python module (mult). Call a py fn() in that module. Runs as a binary
 #   2. c-2-py-1.c:
 #      Runs as a binary. Loads py interpreter to run a python fn() ctime/time given as string
 #   3. c-2-py-2.c,c-2py-3.c:
 #      Python interpreter is ran. C program is loaded as a regular Python module using import.
# Read Makefile:
make
make test
make clean
