#!/bin/env python
# Description:
#   Simple targetted read snoop. uses hash, perfbuffer, info passing b/w entry & exit
# Author: K. Shankar
# Date: May 2020
#

from bcc import BPF

prog="""
#include <uapi/linux/ptrace.h>
#include <linux/sched.h>
#define PASSSIZE 256

typedef struct val {
    u64 id;
    int pid;
    char *buf;
    char ustr[PASSSIZE];
    char comm[TASK_COMM_LEN];
    int ret;
} val_t;

BPF_HASH(info,u64,val_t);
BPF_PERF_OUTPUT(events);

int read_entry(struct pt_regs *ctx,unsigned int fd, char __user *buf, size_t count)
{
    val_t data={};
    data.id = bpf_get_current_pid_tgid();
    data.buf= buf;
    if (fd != 0) return 0; // skip if not stdin
    bpf_get_current_comm(&data.comm, sizeof(data.comm));
    info.update(&data.id, &data);

    return 0;
}

int read_exit(struct pt_regs *ctx)
{
    u64 id = bpf_get_current_pid_tgid();
    val_t *data = info.lookup(&id);
    if (data == 0) {
        return 0; // missed entry
    }
    data->ret = PT_REGS_RC(ctx);
    bpf_probe_read_user(data->ustr,PASSSIZE,data->buf);
    events.perf_submit(ctx, data, sizeof(val_t));
    info.delete(&id);
    return 0;
}
"""

b = BPF(text=prog,debug=0x0)
b.attach_kprobe(event="ksys_read", fn_name='read_entry')
b.attach_kretprobe(event="ksys_read", fn_name='read_exit')

# process event
def print_event(cpu, data, size):
    e = b["events"].event(data)
    print("%d %s %s %d" % (e.id >> 32, e.comm, e.ustr.split(b"\n")[0], e.ret))
    
b["events"].open_perf_buffer(print_event, page_cnt=1024)

while True:
    try:
        b.perf_buffer_poll()
    except KeyboardInterrupt:
        exit()
