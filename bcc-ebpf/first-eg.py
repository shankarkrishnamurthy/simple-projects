#!/usr/bin/env python
from bcc import BPF

program='''
int kprobe__sys_clone(void *ctx)
{
bpf_trace_printk("Hello, World!");
return(0);
}
'''

b = BPF(text=program)
b.trace_print()
