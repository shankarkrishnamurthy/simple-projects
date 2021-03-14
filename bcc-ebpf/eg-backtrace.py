#!/bin/env python
# Descripton:
#   Basic backtraces (user & kernel)
#

from bcc import BPF

prog="""
#include<uapi/linux/ptrace.h>

BPF_PERF_OUTPUT(events);
BPF_STACK_TRACE(bt,8192);

typedef struct val {
    u32 tgid;
    u32 pid;
    u64 ubt;
    u64 kbt;
} val_t;

int pingsend_entry(struct pt_regs *ctx)
{
    val_t data={};
    u64 __pid_tgid = bpf_get_current_pid_tgid();
    data.tgid = __pid_tgid >> 32;
    data.pid = __pid_tgid;
    data.ubt = bt.get_stackid(ctx,BPF_F_USER_STACK);
    data.kbt = bt.get_stackid(ctx,0);
    events.perf_submit(ctx,&data, sizeof(data));

    return 0;
}

"""

b = BPF(text=prog)
b.attach_kprobe(event="ping_v4_sendmsg",fn_name="pingsend_entry")

def print_event(cpu, data, size):
    e = b["events"].event(data)
    print ("pid = ", e.pid)
    al = list(b.get_table("bt").walk(e.ubt))
    print("    USER:")
    for i in al:
        print("\t%#16x"%i,"\t",b.sym(i,e.tgid,show_module=True,show_offset=True))

    al = list(b.get_table("bt").walk(e.kbt))
    print("    KERN:")
    for i in al:
        print("\t%#16x"%i,"\t",b.sym(i,-1,show_module=True,show_offset=True))

b["events"].open_perf_buffer(print_event, page_cnt=1024)
    
while True:
    try:
        b.perf_buffer_poll()
    except KeyboardInterrupt:
        exit()

