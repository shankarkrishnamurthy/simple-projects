import md5
import hashlib
import struct
import binascii

s = 'hello world\n'
m = md5.new() # hashlib.new('md5')
m.update(s)
print m.hexdigest()

#print hashlib.algorithms
d = hashlib.new('sha256')
d.update(s)
print d.hexdigest()

ts = struct.struct(' i 8s f ')
val = (100,'whatever', 2.8)
pts = ts.pack(*val)

print 'Original values:', values
print 'Format string  :', s.format
print 'Uses           :', s.size, 'bytes'
print 'Packed Value   :', binascii.hexlify(packed_data)
