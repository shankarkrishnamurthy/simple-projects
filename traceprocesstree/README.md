# traceprocesstree
show process tree as they are forked/exec'd during runtime

* Use 'as is'

What does it do?
* Problem that this solves is dynamically able to see the process tree thats getting created/destroyed as part of running a program. See eg below. 'ps auxw' or other programs give a snapshot. This captures tree within a duration or by a single program. certainly, there are other ways of doing the same (using kprobes/systemtap, etc) but this definitely serves me as a poor man's tool. 

Caveats?

* Tested on recent linux with fairly recent bash.
* 'ftrace'/python support needs to be there
* Need to have root/sudo

Examples?
* Trace Only particular program:
  - traceprocesstree.sh wireshark-gtk
* Trace all within a duration of T seconds
  - T=8 traceprocesstree.sh

Output?
output of a simple script:
- ./traceprocesstree.sh /usr/sbin/drive_tests.sh 
"/usr/sbin/drive_tests.sh" output > /tmp/tmp.xaVli30632
==========
python /tmp/tmp.eLTzT30633 /tmp/tmp.BDotv30631 30650
 30650 bash
   30651 /bin/bash
     30652 bash
       30653 /usr/sbin/dmidecode
       30656 /bin/cut
       30655 /bin/grep
       30654 /bin/grep

