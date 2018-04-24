#
# Simple Utilities by Shankar Krishnamurthy (Mar 2016)
#
#       **** parse.py ****
# Description: Parsing lspci tree output and making sense out of it. 
#              Output processed output in .dot format
#
# Usage:
#
#   lspci -t | parse.py
# (or)
#   parse.py --file lspci-t.out
# 
# If directly used, it outputs .dot format file which can then
# be passed to render.py below
#
#
#       **** render.py ****
# Dependency:
#    Uses parse.py in additions to few other programs. So, make sure these dependencies are met. Namely, dot, firefox, lspci
#
# usage:
#   render.py (recommmended)
# (or)
#   render.py --raw
# (or)
#   render.py --file /tmp/file.dot
#
#  file = file output from parse.py in .dot format
#  raw = no decoration in terms of tooltip or link speed. (lspci -tv output only)
#  default = calls -vvv output of each device to display additional info
#


