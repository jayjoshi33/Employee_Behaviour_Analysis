    
from flask import Flask, render_template, request
import pickle
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import numpy as np

app = Flask(__name__)
dd = pickle.load(open('dt_model.pkl', 'rb'))
scaler = pickle.load(open('new_scaler.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    EDU = request.form.get('education')
    JY = request.form.get('joining_year')
    PT = request.form.get('payment_tier')
    AGE = request.form.get('age')
    BEN = request.form.get('ever_benched')
    EXP = request.form.get('current_experience')
    G = request.form.get('gender')
    CITY = request.form.get('city')

    Education = 0
    JoiningYear = 0
    PaymentTier = 0
    Age = 0
    EverBenched = 0
    ExperienceInCurrentDomain = 0
    Gender_Male = 0
    City_Delhi = 0
    City_Pune = 0

    if EDU == 'Bachelors':
        Education = 1
    elif EDU == 'Masters':
        Education = 2
    elif EDU == 'PHD':
        Education = 3

    if JY == '2012':
        JoiningYear = 2012
    elif JY == '2013':
        JoiningYear = 2013
    elif JY == '2014':
        JoiningYear = 2014
    elif JY == '2015':
        JoiningYear = 2015
    elif JY == '2016':
        JoiningYear = 2016
    elif JY == '2017':
        JoiningYear = 2017
    else:
        JoiningYear = 2018

        

    if PT == '1':
        PaymentTier = 1
    elif PT == '2':
        PaymentTier = 2
    else:
        PaymentTier=3


    Age = int(AGE)

    if BEN == 'yes':
        EverBenched = 1
    else:
        EverBenched = 0  # Corrected here

    ExperienceInCurrentDomain = float(EXP)

    if G == 'male':
        Gender_Male = 1
    else:
        Gender_Male = 0

    if CITY == 'New Delhi':
        City_Delhi = 1
        City_Pune = 0
    elif CITY == 'Pune':
        City_Pune = 1
        City_Delhi = 0
    else:
        City_Pune = 0
        City_Delhi = 0

    print("Education:", EDU)
    print("Joining Year:", JY)
    print("Payment Tier:", PT)
    print("Age:", AGE)
    print("Ever Benched:", BEN)
    print("Current Experience:", EXP)
    print("Gender:", G)
    print("City:", CITY)

    # Organize inputs into a list
    ip = [Education, JoiningYear, PaymentTier, Age, EverBenched, ExperienceInCurrentDomain, Gender_Male, City_Delhi, City_Pune]

    # Convert the list to a DataFrame
    ip_df = pd.DataFrame([ip], columns=['Education', 'JoiningYear', 'PaymentTier', 'Age', 'EverBenched', 'ExperienceInCurrentDomain', 'Gender_Male', 'City_Delhi', 'City_Pune'])

    # Columns to scale
    columns_to_scale = ['JoiningYear', 'Age', 'ExperienceInCurrentDomain']

    # Transform only the specified columns using the scaler
    ip_df[columns_to_scale] = scaler.transform(ip_df[columns_to_scale])



    # Predict using the model
    prediction = dd.predict(ip_df)[0]
    if prediction==1:
        return render_template('index.html',label=1)
        #'Employee will leave'
    else:
        return render_template('index.html',label=-1)
      
if __name__ == '__main__':
    app.run(debug=True)