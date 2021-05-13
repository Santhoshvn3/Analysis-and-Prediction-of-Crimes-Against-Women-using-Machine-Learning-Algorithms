from re import I
import sys
from flask import Flask, request, render_template, jsonify, session, redirect
from flask.globals import session
from functools import wraps
# import pymongo
# from env.users.models import User
from flask_pymongo import PyMongo
from passlib.hash import sha256_crypt
import uuid

app = Flask(__name__)
app.secret_key = b'\rv\x88\xeb\x97$2\x96\x1f\x02Z)\xc6\x06\xde\xc9'

# database
mongodb_client = PyMongo(app, uri="mongodb://localhost:27017/adminUser")
db = mongodb_client.db

# decorator
def login_required(f):
    @wraps(f)
    def wrap(*arg, **kwargs):
        if 'logged_in' in session:
            return f(*arg, **kwargs)
        else:
            redirect('/')
    return wrap

@app.route('/')
def home():
    return render_template("state.html")

@app.route('/analysis/')
def analysis():
    return render_template("analysis.html")

@app.route('/dashboard/')
@login_required
def dashboard():
    return render_template("dashboard.html")


@app.route('/admin/signup/', methods=['GET', 'POST'])
def admin():
    print('calling signup')
    User().signup()
    return render_template("admin.html") 

@app.route('/admin/login/', methods=['POST', 'GET'])
def adminLogin():
    print('inlogin function')
    user = db.admin1.find_one({
        "email": request.form.get('email')
    })
    if user and request.form.get('password') == user['password']:
        return render_template("alogin.html")
        # return startSession(user)
    # return jsonify({"error": "account doesnot exist"}), 401
@app.route('/admin/signout')
def signout():
    return User().signout()

class User:
    def startSession(self, user):
        del user['passowrd']
        print('session')
        session['logged_in'] = True
        session['user'] = user
        return render_template('alogin.html')

    def signup(self):
        # print(request.form)
        print("in signup function")
        # create user object
        admin = {
            "_id": uuid.uuid4().hex,
            "name": request.form.get('name'),
            "email": request.form.get('email'),
            "password": request.form.get('password')
        }
        # print(jsonify(admin))
        #encrypt password
        # hash_password = sha256_crypt.encrypt(admin['password'])
        # admin['password'] = hash_password
        # print(jsonify(admin))

        #check email exists
        if(db.admin1.find_one({"email" : admin['email']})):
            return jsonify({"error": "email exits"}), 400
        print("saving")
        
        if (db.admin1.save(admin)):
            return self.startSession(admin)       
        
        return jsonify({"error": "Signup failed"})

    def signout(self):
        session.clear()
        return redirect('/')

if __name__ == "__main__":
    # app.init_db()
    app.run(debug=True)
    # app = create_app()
