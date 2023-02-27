from re import I
import sys
from flask import Flask, request, render_template, jsonify, session, redirect, flash
from flask.globals import session
from functools import wraps
from flask.helpers import flash, url_for
# import pymongo
# from env.users.models import User
from sklearn.linear_model import LinearRegression
from flask_pymongo import PyMongo
from passlib.hash import sha256_crypt
import uuid
import hashlib
import pandas as pd
import numpy as np

app = Flask(__name__)
app.secret_key = b'\rv\x88\xeb\x97$2\x96\x1f\x02Z)\xc6\x06\xde\xc9'

# database
#mongodb_client = PyMongo(app, uri="mongodb://localhost:27017/adminUser")
#db = mongodb_client.db


@app.route('/')
def home():
    return render_template("index.html")

@app.route('/analysis.html')
def analysis():

    return render_template('analysis.html')


@app.route('/dashboard/')

def dashboard():
    return render_template("dashboard.html")


@app.route('/admin/signup/')
def admin():
    print('calling signup')

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
#San2 code
@app.route('/pred.html')
def pred():
    return render_template("pred.html")


@app.route('/women.html', methods=['POST'])
def women():
    year = request.form.get("Predict_Year")  # Year fetching From UI.
    C_type = request.form.get("C_Type")  # Crime type fetching from UI
    state = request.form.get("state")  # State name fetching from UI

    df = pd.read_csv("static/StateWiseCAWPred1990-2016.csv", header=None)

    data1 = df.loc[df[0] == state].values  # Selecting State and its attributes.
    for x in data1:
        if x[1] == C_type:
            test = x
            break

    l = len(df.columns)
    trendChangingYear = 2

    xTrain = np.array(
        [2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018,
         2019])
    yTrain = test[2:29]

    X = df.iloc[0, 2:l].values
    y = test[2:]
    regressor = LinearRegression()  # regression algorithm cealled.
    regressor.fit(X.reshape(-1, 1), y)  # Data set is fitted in regression and Reshaped it.
    accuracy = regressor.score(X.reshape(-1, 1), y)  # Finding Accuracy of Predictions.
    print(accuracy)
    accuracy_max = 0.10;

    # Trending year(Influence Year) finding algorithm.
    if (accuracy < 0.10):  # Used 65% accuracy as benchmark for trending year finding algorithm.
        for a in range(3, l - 8):

            X = df.iloc[0, a:l].values
            y = test[a:]
            regressor = LinearRegression()
            regressor.fit(X.reshape(-1, 1), y)
            accuracy = regressor.score(X.reshape(-1, 1), y)
            if (accuracy > accuracy_max):
                accuracy_max = accuracy
                print(accuracy_max)
                trendChangingYear = a
    print(trendChangingYear)  # Printing Trend Changing Year on server terminal.
    print(test[trendChangingYear])
    print(xTrain[trendChangingYear - 2])
    year = int(year)
    y = test[2:]
    b = []

    for j in range(2023, year + 1):
        prediction = regressor.predict(np.array([[j]]))
        if (prediction < 0):
            prediction = 0
        y = np.append(y, prediction)
    y = np.append(y, 0)

    for k in range(2001, year + 1):
        a = str(k)
        b = np.append(b, a)
    y = list(y)
    yearLable = list(b)
    msg = ""
    if C_type == "ASSAULT ON WOMEN WITH INTENT TO OUTRAGE HER MODESTY":
        C_type = "ASSAULT ON WOMEN"
    # Finally the template is rendered
    return render_template('women.html', data=[accuracy, yTrain, xTrain, state, year, data1, X, y, test, l], msg=msg,
                           state=state, year=year, C_type=C_type, pred_data=y, years=yearLable)


#San2 end code
if __name__ == "__main__":
    # app.init_db()
    app.run(debug=True)
    # app = create_app()


