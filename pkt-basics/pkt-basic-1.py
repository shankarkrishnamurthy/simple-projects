import socket
import os, sys
import textwrap
import struct
import signal

class IPv4:
    def __init__(self, raw_data):
        version_header_length = ord(bytes(raw_data[0]))
        self.version = (version_header_length) >> 4
        self.header_length = (version_header_length & 15) * 4
        _,self.total_length =  struct.unpack('2B', raw_data[2:4])
        self.ttl, self.proto, src, target = struct.unpack('! 8x B B 2x 4s 4s', raw_data[:20])
        self.src = self.ipv4(src)
        self.target = self.ipv4(target)
        self.data = raw_data[self.header_length:]

    def ipv4(self, addr): return ''.join([bytes(x).encode('hex') for x in addr])

class TCP:
    def __init__(self, raw_data):
        (self.src_port, self.dst_port, self.sequence, self.acknowledgment, offset_reserved_flags) = struct.unpack(
            '! H H L L H', raw_data[:14])
        offset = (offset_reserved_flags >> 12) * 4
        self.data = raw_data[offset:]

cnt = 0
dh = dict()
def inthandler(c,f):
    print "Exiting ", cnt
    print dh.items()

if __name__ == "__main__":
    signal.signal(signal.SIGINT,inthandler)
    conn = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
    while True:
        raw_data, addr = conn.recvfrom(65535)
        if not raw_data: continue
        ipv4 = IPv4(raw_data)
        tcp = TCP(ipv4.data)
        h=ipv4.src+':'+format(tcp.src_port,'x')+'-'+ipv4.target+':'+format(tcp.dst_port,'x')
        dh[h] = dh.setdefault(h, 0) + ipv4.total_length-ipv4.header_length-20
    #print dh.items()    
     
