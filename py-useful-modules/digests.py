import md5
import hashlib
import struct
import binascii
import ctypes as c

print '\nString => Digests'
s = 'hello world\n'
m = md5.new() # hashlib.new('md5')
m.update(s)
print m.hexdigest()

#print hashlib.algorithms
d = hashlib.new('sha256')
d.update(s)
print d.hexdigest()

print '\nValues => Structs'
val = (100,'whatever', 2.8) # master data

ts = struct.Struct(' i 8s f ')  # @ ! < > =
ts1 = struct.Struct('! i 8s f ') # Network ByteOrder
pts = ts.pack(*val)
pts1 = ts1.pack(*val)

print 'Original values:', val
print 'Format string  :', ts.format
print 'Uses           :', ts.size, 'bytes'
print 'Packed Value   :', binascii.hexlify(pts)
print 'Packed Value   :', binascii.hexlify(pts1)

print '\nStruct => Buffer'
b = c.create_string_buffer(ts.size)
print 'Before(base64 encoded)  :', binascii.b2a_base64(b.raw),
ts.pack_into(b,0,*val)
print 'After(base64 encoded)  :', binascii.b2a_base64(b.raw),
print 'Unpacked:', ts.unpack_from(b, 0)


print '\nBuffer => C'
b = c.create_string_buffer('\0',ts.size)
print 'Before(Hex/Base16) :',binascii.hexlify(b.raw)
_lib = c.CDLL('./libmain.so')
_lib.changestr.argtypes = [c.c_char_p,c.c_int,]
_lib.changestr(b,ts.size)
print 'After(Hex/Base16) :',binascii.hexlify(b.raw)
