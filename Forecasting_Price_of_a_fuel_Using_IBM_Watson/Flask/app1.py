# -*- coding: utf-8 -*-
"""
Created on Sun Apr  3 16:45:56 2022

@author: Hp
"""

import numpy as np #used for numerical analysis
from flask import Flask,render_template,request #Flask is a application used to run/serve our aplication
# request is used to access the file which is uploaded by the user in our application
#render_template is used for rendering the html pages
from tensorflow.keras.models import load_model #we are loading our model from keras
import os

import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "LfURWdM61A46K6WZb4aMGb0WUdif0LvDJc-UZp482TwG"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

app = Flask(__name__) #our flask app

@app.route('/') #rendering html template
def home() :
    return render_template("index.html") #rendering html template
@app.route('/about')
def home1() :
    return render_template("index.html") #rendering html template
@app.route('/predict')
def home2() :
    return render_template("web.html") #rendering html template

@app.route('/login',methods = ['POST']) #route for our prediction
def login() :
    
    a=request.form['year1']
    b=request.form['year2']
    c=request.form['year3']
    d=request.form['year4']
    e=request.form['year5']
    f=request.form['year6']
    g=request.form['year7']
    h=request.form['year8']
    i=request.form['year9']
    j=request.form['year10']#requesting the file
    x_input = [a,b,c,d,e,f,g,h,i,j]
    #x_input=x_input.split(',')
    #print(x_input)
    for i in range(0, len(x_input)): 
        x_input[i] = float(x_input[i]) 
    print(x_input)
    x_input=np.array(x_input).reshape(1,-1)
    temp_input=list(x_input)
    temp_input=temp_input[0].tolist()
    lst_output=[]
    n_steps=10
    i=0
    while(i<1):
        x_input = x_input.reshape((n_steps,1))
        payload_scoring = {"input_data": [{"fields": [["Closing Value"]], "values": [x_input.tolist()]}]}
        response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/969497ff-c61a-4ae2-a1c7-162e0679e41f/predictions?version=2022-04-03', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
        yhat =response_scoring.json()
        i=i+1
        yhat=yhat['predictions'][0]['values'][0][0]
        return render_template('web.html',showcase = 'The next day predicted value is : '+str(yhat))
    #return str(x)
    
if __name__ == '__main__' :
    #app.run(debug = True,port=5000)
    port = int(os.environ.get('PORT',5000))
    app.run(port = port, debug = True, use_reloader = False)