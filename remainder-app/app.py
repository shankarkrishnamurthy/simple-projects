#!/bin/env python
from flask import Flask, render_template, request, jsonify,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from db import *
from driver import *
from threading import Thread
from flask_login import LoginManager,login_user,logout_user,login_required,current_user
from user import *

app = Flask(__name__)
CORS(app)
db = DB()
driver = driver(db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
app.secret_key = 'not so secret, is it?'

@login_manager.user_loader
def load_user(user_id):
    if user_id in users: return User(user_id)
    return None
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        n = request.form["username"] 
        u = User(n) if n in users else None
        if u: 
            login_user(u)
            return redirect(url_for("index"))
    return render_template('login.html')
@app.route('/logout', methods=['GET','POST'])
def logout():
    logout_user()
    print('getting to this url ' ,url_for("index"))
    return redirect(url_for('index'))

@app.route('/')
@login_required
def index():
    return render_template('home.html',name=current_user.name)

@app.route('/item', methods=['POST', 'GET'])
@login_required
def data():
    if request.method == 'POST':
        msg=request.form['descr']+' (Exp Date : '+request.form['infodate']+')'
        db.create(msg, request.form['fdate'])
        return render_template('home.html',name=current_user.name)

    if request.method == 'GET':
        return render_template('home.html', list=db.getall(),name=current_user.name)
        
@app.route('/item/<id>', methods=['DELETE'])
@login_required
def deldata(id):
    db.delete(id)
    return render_template('home.html', list=db.getall(),name=current_user.name) 

t = Thread(target=driver.eventloop, )
t.daemon = True
t.start()

if __name__ == '__main__':
    app.debug = True
    app.run()
