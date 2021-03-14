#!/bin/env bash
#
# Description:
#       Simple script to dynamically see the children/ancestry of process tree. 
# For more, refer to README
#
# By Shankar Krishnamurthy
#

if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

function cleanup ()
{
    [[ -n "$MOUNT" ]] && umount $MDIR
    #rm $TFILE $FOUT $POUT
}

function initfn () 
{
    MDIR=/sys/kernel/debug/
    TDIR=$MDIR/tracing
    FOUT=$(mktemp)
    POUT=$(mktemp)
    TFILE=$(mktemp)
    if [[ ! -d "$TDIR" ]]; then
        MOUNT=1
        mount -t debugfs none $MDIR
    fi
}
function clrtrap ()
{
    trap '' INT
}
function settrap ()
{
    trap "cleanup; exit" INT
}

T=${T:-10}
PROG="$@"; #echo $PROG
settrap

initfn

echo 0 > $TDIR/tracing_on ;
echo 1 | tee $TDIR/events/sched/sched_process_fork/enable \
       | tee $TDIR/events/sched/sched_process_exit/enable \
       | tee $TDIR/events/sched/sched_process_exec/enable 1>/dev/null
> $TDIR/trace; 
echo 1 > $TDIR/tracing_on ;

clrtrap
if [[ -z "$PROG" ]];  then
    echo "Sleep for $T seconds"
    sleep $T
else
    # program to run
    echo \"$PROG\" output \> $POUT 
    eval $PROG 2>&1 >$POUT& 
    PID=$!
    #echo PID=$PID
    wait
fi
settrap 

echo 0 > $TDIR/tracing_on ;
cat $TDIR/trace > $FOUT
echo 0 | tee $TDIR/events/sched/sched_process_fork/enable \
       | tee $TDIR/events/sched/sched_process_exit/enable \
       | tee $TDIR/events/sched/sched_process_exec/enable 1>/dev/null


cat <<END > $TFILE
#!/usr/bin/python

import sys, os
import re

def uniq_append(l, pid):
    s = set(l)
    s.add(pid)
    return list(s)

def handle_fork(line, tree, pids):
    m = re.search(r'\s+(\S+)-(\d+)\s+\[\d+\] .{4} \d+.\d+: sched_process_fork: comm=\S+ pid=\d+ child_comm=(\S+) child_pid=(\d+)$', line)
    if not m:
        return pids
    #print m.group(0) # has whole line
    comm = m.group(1)
    pid = m.group(2)
    childcomm = m.group(3)
    childpid = m.group(4)

    if tree.has_key(pid):
        obj = tree[pid]
        obj['children'] = uniq_append(obj['children'], childpid)
    else:
        obj = {}
        obj['pid'] = pid
        obj['parent'] = "-1"
        obj['children'] = []
        obj['comm'] = comm
        tree[pid] = obj
    obj = {}
    obj['pid'] = childpid
    obj['parent'] = pid
    obj['children'] = []
    obj['comm'] = childcomm
    tree[childpid] = obj

    # attach new pid to interesting pid list
    if specificpid == 1:
        pids = uniq_append(pids, childpid)
    return pids

def handle_exec(line, tree, pids):
    m = re.search(r'\s+(\S+)-(\d+)\s+\[\d+\] .{4} \d+.\d+: sched_process_exec: filename=(\S+) pid=(\d+) old_pid=(\d+)$', line)
    if not m:
        return pids
    #print m.group(0) # has whole line
    comm = m.group(1)
    realpid = m.group(2)
    filename = m.group(3)
    pid = m.group(4)
    oldpid = m.group(5)

    # start : conditions we will handle later
    if realpid == pid and pid == oldpid:
        pass
    else:
        print "Exec is strange: its ptrace'd?"
        raise Exception("Cannot handle")
    if not tree.has_key(pid):
        print tree
        raise Exception("Cannot handle. Exec of unknown pid")
    # end
    obj = tree[realpid]
    obj['comm'] = filename
    return pids

def main(file, pids):
    tree={}
    f = open(file, 'r')
    try:
        for line in f:
            if specificpid == 1:
                m = re.findall(r"(?=("+'|'.join(pids)+r"))",line)
                if not m:
                    continue

            pids = handle_fork(line, tree, pids)

            pids = handle_exec(line, tree, pids)

            if re.search('sched_process_exit:', line):
                # print "exit line: " + line
                # not used currently
                pass

    finally:
        f.close()
    return tree

def prettyprint(tree, root, indent):
    
    if not tree.has_key(root):
        return

    obj = tree[root]
    pid = obj['pid']
    comm = obj['comm']
    print "%s %s %s" % (indent, pid, comm)

    indent+="  "

    for pid in obj['children']:
        prettyprint(tree, pid, indent)

    return

if __name__ == '__main__':
    # len=1 - Only Program name; len=2 - One arg given 
    if len(sys.argv) < 2:
        print "Insuffient argument.\nUsage:\n\t Prog <file> <rootpid>"
        sys.exit(1)
    pids=[]
    specificpid=0
    if len(sys.argv) > 2:
        pids = [sys.argv[2]]
        specificpid=1
    file = sys.argv[1]

    tree = main(file, pids)
    #print tree
    if specificpid == 0:
        for pid in tree:
            prettyprint(tree, pid, "")
    else:
        prettyprint(tree, pids[0], "")

END

printf '=%.0s' {1..10}
echo
echo python $TFILE $FOUT $PID
python $TFILE $FOUT $PID

cleanup
