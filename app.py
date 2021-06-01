from re import I
import re
import sys, os
from flask import Flask, request, render_template, jsonify, session, redirect, flash
from flask.globals import session
from re import I
from functools import wraps
from flask.helpers import flash, url_for
from flask.wrappers import Request
from flask_mail import Mail, Message
from random import *
from sklearn.linear_model import LinearRegression
from flask_pymongo import PyMongo
from passlib.hash import sha256_crypt
import uuid
import hashlib
import pandas as pd
import numpy as np
from .local_settings import password

app = Flask(__name__)
# app = Flask(static_folder='/home/vinay/APCW/env/static')
app.secret_key = b'\rv\x88\xeb\x97$2\x96\x1f\x02Z)\xc6\x06\xde\xc9'

# mail config
mail = Mail(app)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = ''
app.config['MAIL_PASSWORD'] = password()
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
otp = int(randint(000000, 999999))

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
    return render_template("index.html")

@app.route('/state/')
def state():
    return render_template("state.html")

@app.route('/analysis/',methods=['GET', 'POST'])
def analysis():
    return render_template("analysis.html")

@app.route('/dashboard/')
@login_required
def dashboard():
    return render_template("dashboard.html")

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/admin/signup/', methods=['GET', 'POST'])
def admin():
    print('calling signup')
    if request.method == 'GET':
        return render_template("admin.html") 
    elif request.method == 'POST':
        return User().signup()

@app.route('/admin/login/', methods=['GET', 'POST'])
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
            # flash("login successful", "success")
            return render_template("dashboard.html")
        else:
            flash("Email or Password Is Incorrect", "warning")
            return redirect(request.url)
@app.route('/admin/signout/')
def signout():
    return User().signout()


@app.route('/admin/forgotpassword/', methods=['GET', 'POST'])
def forgotPassword():
    if request.method == "POST":
        url = request.host_url + 'admin/resetPassword/'
        email1 = request.form.get('email')
        if not email1:
            flash('please enter email')
            return (request.url)
        # email1 = str(email1)
        email_found = db.admin1.find({"email": email1}).count() > 0
        print("email found is",email_found)
        if email_found > 0:
            msg = Message(subject="reset password from analysis and prediction of crime against women", sender="vinaybhathg11@fmail.com", recipients=[email1])
            msg.body = url
            mail.send(msg)
            flash("email sent successfully", "success")
        else:
            flash("email not exists", "warning")
            return redirect(request.url)
    return render_template('forgot_password.html')

@app.route('/admin/resetPassword/', methods=['GET', 'POST'])
def resetPassword():
    if request.method == 'POST':
        email1 = request.form.get('email')
        user_password = request.form.get('cpassword')
        if user_password:
            hash_password = hashlib.md5(user_password.encode('utf-8'))
            user_password = hash_password.hexdigest()
        # user_email =  db.admin1.find({"email": email1})
        print("email found reset", email1)
        flag = db.admin1.find_one_and_update({"email": email1}, { "$set": {"password": user_password}})
        print('updation', flag)
        if (flag):
            flash("password reset sucessfull login with new password", "success")
    return render_template('reset_password.html')


@app.route('/admin/verify/', methods=['GET', 'POST'])
def verifyEmail(email):
    # email = request.form.email()
    msg = Message(subject="OTP from Analysis and Prediction of Crime Against Women", sender="vinaybhathg11@gmail.com", recipients=[email])
    msg.body = str(otp)
    mail.send(msg)
    return render_template('verify.html')

@app.route('/admin/verfiylogin/', methods=['GET', 'POST'])
def verfiyAdmin():
    return render_template("dashboard.html")
    # else:
    #     print('inlogin function')
    #     user = db.admin1.find_one({
    #         "email": request.form.get('email')
    #     })
    #     user_password = request.form.get('password')
    #     if user_password:
    #         user_password = hashlib.md5(user_password.encode('utf-8')).hexdigest()
    #     if user and user_password == user['password']:
    #         # flash("login successful", "success")
    #         return render_template("dashboard.html")
    #     else:
    #         flash("Email or Password Is Incorrect", "warning")
    #         return redirect(request.url)
    # return render_template('alogin.html')

@app.route('/admin/validate/', methods=['GET', 'POST'])
def validate():
    if request.method == 'POST':
        print('inside if')
        user_otp = request.form.get('pin')
        if otp == int(user_otp):
            flash('Email verification successfull', "success")
            # if request.method == 'GET':
            return verfiyAdmin()
        else:
            flash('Email verification failed', "warning")
            return render_template('verify.html')
    

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

        if admin['name'] == None or admin['email'] == 'None' or admin['password'] == None:
            return redirect(request.url)
        else:
            password = admin['password']
            if password:
                hash_password = hashlib.md5(admin['password'].encode('utf-8'))
                admin['password'] = hash_password.hexdigest()
            # print(jsonify(admin))

            #check email exists
            if(db.admin1.find_one({"email" : admin['email']})):
                flash("Email Id Already Exists", "warning")
                return redirect(request.url)
            print("saving")
            
            if (db.admin1.save(admin)):
                flash('Registered Successfully', "success")
                # return self.startSession(admin)
                return verifyEmail(admin['email'])
                # return render_template("alogin.html")       
            
            return flash('Sign Up Failed!!', "warning")

    def signout(self):
        session.clear()
        return redirect('/')

@app.route('/prediction/')
def pred():
    return render_template("pred.html")

@app.route('/women', methods=['GET','POST'])
def women():
    year = request.form.get("Predict_Year")	#Year fetching From UI.
    C_type = request.form.get("C_Type")	#Crime type fetching from UI
    state = request.form.get("state")	#State name fetching from UI
    
    df = pd.read_csv("static/StateWiseCAWPred1990-2019.csv", header=None)

    data1 = df.loc[df[0]==state].values			#Selecting State and its attributes.
    for x in data1:
	    if x[1] == C_type:
		    test = x
		    break
    
    l = len(df.columns)
    trendChangingYear = 2

    xTrain = np.array([2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019])
    yTrain = test[2:29]

    X = df.iloc[0,2:l].values
    y = test[2:]
    regressor = LinearRegression()		#regression algorithm cealled.
    regressor.fit(X.reshape(-1,1),y)	#Data set is fitted in regression and Reshaped it.
    accuracy = regressor.score(X.reshape(-1,1),y)	#Finding Accuracy of Predictions.
    print (accuracy)
    accuracy_max = 0.10;

	#Trending year(Influence Year) finding algorithm.
    if(accuracy < 0.50):			#Used 65% accuracy as benchmark for trending year finding algorithm.
        for a in range(3,l-8):
            X = df.iloc[0,a:l].values
            y = test[a:]
            regressor = LinearRegression()
            regressor.fit(X.reshape(-1,1),y)
            accuracy = regressor.score(X.reshape(-1,1),y)
            if (accuracy > accuracy_max):
                accuracy_max = accuracy
                print (accuracy_max)
                trendChangingYear = a
    print (trendChangingYear)			#Printing Trend Changing Year on server terminal.
    print (test[trendChangingYear])
    print (xTrain[trendChangingYear-2])
    year = int(year)
    y = test[2:]
    b = []

	#If accuracy is Lower than 65%, only visualization of the data is shown - no predictions
    if accuracy < 0.50:
        for k in range(2001,2019):
            a = str(k)
            b = np.append(b,a)
        y = list(y)
        yearLable = list(b)
        msg = "Data is not Sutaible for prediction"

	#Else predictions are shown and Run time data and labels are added to the graph.
    else:
        for j in range(2021,year+1):
            prediction = regressor.predict(np.array([[j]]))
            if(prediction < 0):
                prediction = 0
            y = np.append(y,prediction)
        y = np.append(y,0)
        
        for k in range(2001,year+1):
            a = str(k)
            b = np.append(b,a)
        y = list(y)
        yearLable = list(b)
        msg = ""
    if C_type == "ASSAULT ON WOMEN WITH INTENT TO OUTRAGE HER MODESTY":
        C_type = "ASSAULT ON WOMEN"
	#Finally the template is rendered
    return render_template('women.html',data = [accuracy,yTrain,xTrain,state,year,data1,X,y,test,l],msg = msg,state=state, year=year, C_type=C_type,pred_data = y,years = yearLable)

if __name__ == "__main__":
    # app.init_db()
    app.run(debug=True)
    # app = create_app()


