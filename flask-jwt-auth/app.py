from flask import Flask,request,jsonify,make_response,render_template
import jwt
from datetime import datetime, timedelta
from functools import wraps
   
app = Flask(__name__)
app.config['SECRET_KEY'] = 'not so secret key. is it?'

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message' : 'Token is missing !!'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            print(data)
            current_user = data['public_id']
        except:
            return jsonify({ 'message' : 'Token is invalid !' }), 401

        return  f(current_user, *args, **kwargs)
    return decorated

@app.route('/login', methods =['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    auth = request.form
    print(auth)
    if not auth:
        return make_response('Could not verify',401,{'WWW-Authenticate':'Failed'})
   
    if 'username' in auth:
        token = jwt.encode({ 'public_id': auth['username'], 'exp' : datetime.utcnow()+timedelta(minutes=1) }, app.config['SECRET_KEY'])
        return make_response(jsonify({'token' : token.decode('UTF-8')}), 201)

    return make_response('Could not verify',403,{'WWW-Authenticate' : 'Failed!'})

@app.route('/')
@token_required
def main(r):
    return render_template('home.html')

if __name__ == "__main__":
    app.run(debug = True,port=3142)
