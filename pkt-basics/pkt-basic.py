import socket
import os, sys
import textwrap
import struct
import signal

def get_mac_addr(mac_raw):
    mac_addr = [bytes(x).encode('hex') for x in mac_raw]
    return ':'.join(mac_addr).upper()

def format_multi_line(prefix, string, size=80):
    size -= len(prefix)
    if isinstance(string, bytes):
        string = ''.join(r'\x{:02x}'.format(byte) for byte in string)
        if size % 2:
            size -= 1
    return '\n'.join([prefix + line for line in textwrap.wrap(string, size)])

class Ethernet:
    def __init__(self, raw_data):
        dest, src, prototype = struct.unpack('! 6s 6s H', raw_data[:14])
        #self.dest_mac = get_mac_addr(dest)
        #self.src_mac = get_mac_addr(src)
        self.proto = socket.htons(prototype)
        self.data = raw_data[14:]

class IPv4:
    def __init__(self, raw_data):
        version_header_length = ord(bytes(raw_data[0]))
        self.version = (version_header_length) >> 4
        self.header_length = (version_header_length & 15) * 4
        self.ttl, self.proto, src, target = struct.unpack('! 8x B B 2x 4s 4s', raw_data[:20])
        #self.src = self.ipv4(src)
        #self.target = self.ipv4(target)
        self.data = raw_data[self.header_length:]

    def ipv4(self, addr): return '.'.join([str(int(bytes(x).encode('hex'),16)) for x in addr])

class TCP:
    def __init__(self, raw_data):
        (self.src_port, self.dst_port, self.sequence, self.acknowledgment, offset_reserved_flags) = struct.unpack(
            '! H H L L H', raw_data[:14])
        offset = (offset_reserved_flags >> 12) * 4
        self.flag_urg = (offset_reserved_flags & 32) >> 5
        self.flag_ack = (offset_reserved_flags & 16) >> 4
        self.flag_psh = (offset_reserved_flags & 8) >> 3
        self.flag_rst = (offset_reserved_flags & 4) >> 2
        self.flag_syn = (offset_reserved_flags & 2) >> 1
        self.flag_fin = offset_reserved_flags & 1
        self.data = raw_data[offset:]

cnt = 0
def inthandler(c,f):
    print "Exiting ", cnt

if __name__ == "__main__":
    signal.signal(signal.SIGINT,inthandler)
    conn = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
    while True:
        raw_data, addr = conn.recvfrom(65535)
        if not raw_data: continue
        eth = Ethernet(raw_data)
        if eth.proto != 8: continue
        #print(eth.dest_mac, eth.src_mac, eth.proto)

        ipv4 = IPv4(eth.data)
        if ipv4.proto != 6: continue
        #print(ipv4.version, ipv4.header_length, ipv4.ttl)
        #print(ipv4.proto, ipv4.src, ipv4.target)

        #tcp = TCP(ipv4.data)
        #print ipv4.src + ':' + str(tcp.src_port), ipv4.target + ':' + str(tcp.dst_port)

        cnt += 1
        
