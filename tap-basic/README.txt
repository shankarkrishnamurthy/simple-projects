tap-basic
=========

  This file is written for my own reference and to document the subtle differences in usage of tap device in linux kernel
  Ref: drivers/net/tun.c
  
  Basic structure: 
     Ethernet frame is sent to tap interface directly using sendto() socket. Another process (forked) receives the message (using tap fd and a 'read' call) and retransmits (using write on tap fd) into another tap device.
     
     The resulting frame is finally recv'd by the original process (which used sendto) using recvfrom() socket call.
     
  Basic Idea to Note:
    The sendto() socket call behaves fundamentally different from 'write' call on tap fd. While sendto() calls kernel tap/tun transmit fn(), the 'write' call ends up calling netif_rx (recv fn()).
    
    --Shankar Krishnamurthy
    
    
