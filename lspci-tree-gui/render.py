#!/bin/env python
#
# Dependency:
#    Uses parse.py. So, make sure this dependency is met
#
# usage:
#   render.py --tree <lspci-t.out> --ancestory <bdf>
#   render.py --tree <lspci-t.out>
#
#   render.py --dotfile /tmp/eg.dot
#   render.py --ancestory <bdf>
#
#   <Deprecated> render.py
#   <Deprecated> render.py --all (applicable only on LIVE system)
#

import os, re
import sys, time
import subprocess
import tempfile
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

    f.write("\""+node.parent.bdf()+"\" -- \""+ node.bdf()+ "\"\n")
    """
    if options.all:
        label, edge,tooltip = get_edge(node) # LnkSta (if non zero)
        if len(edge) != 0:
            #f.write("\""+node.bdf()+"\" [ URL=\"" + url + "\" ]\n")
            f.write("\""+node.bdf()+"\" [ label=" + label + " tooltip=\"" + tooltip + "\" ]\n")
            f.write("\""+node.parent.bdf()+"\" -- \""+ node.bdf()+ "\"" + edge + "\n")
    """

def create_ancestory(dot):
    def find_parent(s,c):
        for i in s:
            r = re.compile('"(.*)" -- "(%s)"' % c)
            m = r.match(i)
            if m:
                p = m.groups()[0]
                return p,i
        return None,None

    r = re.compile('[0-9a-fA-F]{2}:[0-9a-fA-F]{2}\.\d')
    if r.match(options.ancestory) is None:
        print 'Enter value BDF. Format BB:DD.F', options.ancestory
        sys.exit(0)
    mdf = open(dot, "r")
    out = mdf.read().splitlines()
    mdf.close()
    dot = tempfile.mktemp()
    print "Create temperarary dotfile %s for ancestory only" % dot
    mdf = open(dot, "w")
    mdf.write("graph lspci {\n")
    child, parent = options.ancestory, ''
    while True:
        parent,dl = find_parent(out, child)
        if parent == child or not parent : break
        mdf.write(dl + "\n")
        child = parent
    mdf.write("}\n")
    mdf.close()
    return dot

#
# Main:
#
parser = optparse.OptionParser()
#parser.add_option('-a', '--all', default=False, action="store_true", help="includes all including devices w/ width=0" )
parser.add_option('-d', '--dotfile', help="dot filename with path for rendering" )
parser.add_option('--nogui', default=False,  action="store_true",  help="dot filename with path for rendering" )
parser.add_option('--tree', help="filename with lspci -tv output" )
parser.add_option('--ancestory', help="filename with lspci -tv output" )
options, remainder = parser.parse_args()

if options.dotfile:
    dot = options.dotfile
    print ".dot file is not Generated. GUI directly rendered from given .dot file."

else:                   # generate a dot file on the fly
    # convert string to tree format
    tokenslist=[]
    if options.tree:
        myfile = open(options.tree, 'r')
        out = myfile.read().splitlines()
    else:
        out = exec_cmd("lspci -t")
        print "Using lspci-t output from live (current) system"

    for st in out:
        miter = tokenize(st)
        tokenslist.append(miter)
    process(tokenslist)
    Root = parse.Root
    
    # write dot file
    dot="/tmp/eg.dot"
    f=open(dot, "w")
    f.write("graph lspci {\n")
    for n in Root.children: walk(n)
    f.write("}\n")
    f.close()
    print "Generated .dot file from lspci-t output ", dot

if options.ancestory:
    dot = create_ancestory(dot)
      
if not options.nogui:
    # write svg file - dot always rights to current dir
    svg="/tmp/eg.svg"
    cmd="/usr/bin/dot -Tsvg -o" + svg + " " + dot + " 2>/dev/null"
    print "Executing ", cmd
    os.system(cmd)
    if not os.path.isfile(svg):
        print "copy ",dot, " where 'dot' appl is available"
        sys.exit()
    
    # render it in firefox
    cmd = "firefox "+svg+" & "
    os.system(cmd)

