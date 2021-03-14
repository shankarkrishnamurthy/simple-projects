from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from db import *
from driver import *
from threading import Thread

app = Flask(__name__)
CORS(app)
db = DB()
driver = driver(db)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/item', methods=['POST', 'GET'])
def data():
    if request.method == 'POST':
        msg=request.form['descr']+' (Exp Date : '+request.form['infodate']+')'
        db.create(msg, request.form['fdate'])
        return render_template('home.html')

    if request.method == 'GET':
        rc = db.getall()
        return render_template('home.html', list=rc)
        
@app.route('/item/<id>', methods=['DELETE']) 
def deldata(id):
    db.delete(id)
    return render_template('home.html', list=db.getall()) 

t = Thread(target=driver.eventloop, )
t.daemon = True
t.start()

if __name__ == '__main__':
    app.debug = True
    app.run()
