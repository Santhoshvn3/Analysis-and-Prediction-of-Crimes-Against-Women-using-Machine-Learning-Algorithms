from re import I
import sys
from flask import Flask, request, render_template, jsonify, session, redirect, flash
from flask.globals import session
from functools import wraps
from flask.helpers import flash, url_for
# import pymongo
# from env.users.models import User
from flask_pymongo import PyMongo
from passlib.hash import sha256_crypt
import uuid
import hashlib

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
    if request.method == 'GET':
        return render_template("alogin.html")
    else:
        print('inlogin function')
        user = db.admin1.find_one({
            "email": request.form.get('email')
        })
        user_password = request.form.get('password')
        if user_password:
            user_password = hashlib.md5(user_password.encode('utf-8')).hexdigest()
        if user and user_password == user['password']:
            print('login successful')
            return render_template("dashboard.html")
        else:
            flash('Email Or Password Is Incorrect')
        # return startSession(user)
    # return jsonify({"error": "account doesnot exist"}), 401
@app.route('/admin/signout')
def signout():
    return User().signout()

class User:
    def startSession(self, user):
        del user['password']
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
        # if admin['email']:
        #     flash('email already exists')
        password = admin['password']
        if password:
            hash_password = hashlib.md5(admin['password'].encode('utf-8'))
            admin['password'] = hash_password.hexdigest()
        # print(jsonify(admin))

        #check email exists
        if(db.admin1.find_one({"email" : admin['email']})):
            flash('Email Id Already Exists')
        print("saving")
        
        if (db.admin1.save(admin)):
            flash('Registered Successfully')
            return self.startSession(admin)       
        
        return flash('Sign Up Failed!!')

    def signout(self):
        session.clear()
        return redirect('/')

if __name__ == "__main__":
    # app.init_db()
    app.run(debug=True)
    # app = create_app()


