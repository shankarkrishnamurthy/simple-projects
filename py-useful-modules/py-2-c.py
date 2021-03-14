#!/bin/python

from ctypes import *
import binascii

_lib = CDLL("./libmain.so")

# call fn(): Integer arg and Int return value (default)
print("\nPy -> C simple fn call")
print("val: %d\n" % _lib.square(10))

# String/char* arg. return void
print('\nBuffer => C')
b = create_string_buffer(b'\0',16)
print('Before(Hex/Base16) :',binascii.hexlify(b.raw))
_lib.changestr.argtypes = [c_char_p,c_int,]     # arg type
_lib.changestr.restype = c_char_p               # return type
s = _lib.changestr(b,16)                        # call fn()
print('After(Hex/Base16) ',binascii.hexlify(b.raw),'\narg bytes ', b.value, '\nreturn bytes ', s)

# struct => 'C' => struct back
class MyStruct(Structure):
    _fields_ = [('v', c_double),
                ('t', c_int),
                ('c', c_char_p)]
_lib.getstruct.restype = POINTER(MyStruct)
_lib.getstruct.argtypes = [POINTER(MyStruct)]   # list even if its only 1
a = pointer(MyStruct(39.7,101,b"deadbeef"))     # note: pointer vs POINTER
y = _lib.getstruct(a)                           # call fn()
x = y.contents                                  # 'secret' dereferencing  <=> x = *y
print("Py: v ", x.v,"t ",x.t,"c ",x.c,"\n")


print("\nPython array of Dict => C struct array")
class CA(Structure):
    _fields_ = [('Keys',c_char_p),
                ('Values',POINTER(c_float)),
                ('Title',c_char_p),
                ('Index',c_int)]
Tmp={'Name1': [10.0, 20.0, 'Title1', 1], 'Name2': [5.0, 25.0, 'Title2', 2]}
ca_list = []
for k,v in Tmp.items():
    ca = CA()
    ca.Keys = k.encode('utf8') # Python 3 strings are Unicode, char* needs a byte string
    ca.Values = (c_float*2)(v[0],v[1]) # Interface unclear, how would target function know how many floats?
    ca.Title = v[2].encode('utf8')
    ca.Index = v[3]
    ca_list.append(ca)

ca_array = (CA * len(ca_list))(*ca_list) # python list of CAs => C type array of CAs
_lib.myfunc(ca_array,len(ca_array)) # call fn()
