#!/bin/env python
from random import randint
from time import sleep

from flask import request
from flask import Flask
app = Flask(__name__)

counter_value = 1

def get_counter():
    return str(counter_value)

def increase_counter():
    global counter_value
    int(counter_value)
    sleep(randint(1,10))
    counter_value += 1
    return str(counter_value)

@app.route('/api/counter', methods=['GET', 'POST'])
def counter():
    if request.method == 'GET':
        return get_counter()
    elif request.method == 'POST':
        return increase_counter()
