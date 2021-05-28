from flask import Flask ,render_template
from flask import request

from flask import Flask,render_template, request, flash, url_for,jsonify
import pandas as pd
import numpy as np
from flask import json
from sklearn import preprocessing
from sklearn.linear_model import LinearRegression
import joblib
from sklearn.ensemble import RandomForestRegressor
from plotly.offline import init_notebook_mode, iplot

app = Flask(__name__)

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/analysis.html')
def analysis():

    return render_template('analysis.html')

@app.route('/year_analysis.html')
def year_analysis():

    return render_template('year_analysis.html')

@app.route('/state.html')
def state():

    return render_template('state.html')

@app.route('/pred.html')
def pred():
	return render_template("pred.html")

@app.route('/women.html',methods = ['POST'])
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


if __name__ == '__main__':
    app.run(debug = True)
