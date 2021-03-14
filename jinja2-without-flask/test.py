#!/bin/env python

from jinja2 import *

file_loader = FileSystemLoader(".")
env = Environment(loader=file_loader)
template = env.get_template('text.tpl')
data = {"name": "shankar", "animal":"lamb" , "truth":False, "colors":["red","blue","green"]}
output = template.render(data = data,name="hdr")
print(output)
