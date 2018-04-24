#!/bin/env python
#
# Dependency:
#    Uses parse.py in additions few other programs. So, make sure these dependencies are met
#    Namely, dot, firefox, lspci
#
# usage:
#   render.py (recommmended)
# (or)
#   render.py --raw (use '-h' to see what these means)
#
#  raw = no decoration in terms of tooltip or link speed. (lspci -tv output only)
#  default = calls -vvv output of each device to display additional info
#

import os
import sys, time
import subprocess
sys.path.insert(0,os.path.dirname(os.path.realpath(__file__)))
import parse
from parse import *

def exec_cmd(cmd):
    """Executes a shell command and returns the output as a list."""
    out, err = subprocess.Popen(cmd, shell=True,
                                stdout=subprocess.PIPE).communicate()
    return out.splitlines()

def get_edge(n):
    edge = ""
    lstr = ""
    out = exec_cmd("lspci -vv -s "+n.bdf())
    tt ="<" + "<BR/>\n".join(out) + ">"
    for s in out:
        pat = "%s (.*): " % n.bdf()
        m = re.search( pat, s)
        if m:
            cstr = m.groups()[0]
            lstr = "<" + n.bdf() +  "<BR/>\n<FONT POINT-SIZE=\"8\">" + cstr + "</FONT>>"

        m = re.search( r'LnkSta:\sSpeed (.*), Width (.*),',s)
        if m:
            speed =  m.groups()[0]
            width =  m.groups()[1]
            #if len(width) != 0 and len(speed) != 0:
            if options.all or width != "x0": # and speed != "unknown":
                edge = "[ label = \"" + speed + ":" + width + "\" ]"
            return (lstr, edge,tt)
    return (lstr, edge,tt)

def walk(node):
    for n in node.children:
        walk(n)

    if options.raw:
        f.write("\""+node.parent.bdf()+"\" -- \""+ node.bdf()+ "\"\n")
    else:
        label, edge,tooltip = get_edge(node) # LnkSta (if non zero)
        if len(edge) != 0:
            #f.write("\""+node.bdf()+"\" [ URL=\"" + url + "\" ]\n")
            f.write("\""+node.bdf()+"\" [ label=" + label + " tooltip=\"" + tooltip + "\" ]\n")
            f.write("\""+node.parent.bdf()+"\" -- \""+ node.bdf()+ "\"" + edge + "\n")

#
# Main:
#
parser = optparse.OptionParser()
parser.add_option('--file', help="Takes in .dot format file" )
parser.add_option('-r', '--raw', default=False, action="store_true", help="raw output no decoration" )
parser.add_option('-a', '--all', default=False, action="store_true", help="includes all including devices w/ width=0" )
options, remainder = parser.parse_args()

# global settings
prog = 'firefox'
formattype = 'svg'
convprog='/usr/bin/dot'

if not options.file:
    # convert string to tree format
    tokenslist=[]
    out = exec_cmd("lspci -t")
    for str in out:
        miter = tokenize(str)
        tokenslist.append(miter)
    process(tokenslist)
    Root = parse.Root

    # write dot file
    dotfile="/tmp/eg.dot"
    f=open(dotfile, "w")
    f.write("graph lspci {\n")
    for n in Root.children:
        walk(n)
    f.write("}\n")
    f.close()
else:
    dotfile = options.file
      
# write file - dot always rights to current dir
ofile="/tmp/eg." + formattype
cmd=convprog + " -T" + formattype + " -o" + ofile + " " + dotfile + " 2>/dev/null"
print cmd
os.system(cmd)
if not os.path.isfile(ofile):
    print "Outfile Creation Failed ", ofile
    sys.exit()

# render
cmd = prog+" "+ofile+" & "
os.system(cmd)

