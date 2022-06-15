# Import libraries
import re
import numpy as np
from flask import Flask, request, jsonify, render_template,redirect
import pickle
import math as math

app = Flask(__name__)

# Load the model
# lr_model = pickle.load(open('models.pkl', 'rb'))
# rf_classifier = pickle.load(open('models.pkl', 'rb'))

all_models=pickle.load(open('models.pkl', 'rb'))
all_models2=pickle.load(open('models.pkl', 'rb'))

@app.route('/', methods=['GET', 'POST'])
def hello():
    return render_template("index.html")
@app.route('/aboutUs',methods=['GET'])
def aboutUs():
    return render_template('aboutUs.html')
# @app.route('/submitform', methods = ['POST'])
# def submitform():
#     name = request.form['name']
#     email= request.form['email']
#     age=request.form['age']
#     sex=request.form['gender']
#     cp=request.form['cp']
#     trestbps=request.form['trestbps']
#     chol=request.form['chol']
#     fbs=request.form['fbs']
#     restecg=request.form['restecg']
#     thalach=request.form['thalach']
#     exang=request.form['exang']
#     oldpeak=request.form['oldpeak']
#     thal=request.form['thal']
#     print("The email address is '" + age + "|"+sex)
#     # return redirect('/api/{age}/{sex}/{cp}/{trestbps}/{chol}/{fbs}/{restecg}/${thalach}/${exang}/${oldpeak}/${thal}')
#     return redirect()
    
@app.route('/api', methods=['GET', 'POST'])
def predict():
    name = request.form['name']
    email= request.form['email']
    age=request.form['age']
    fgender=request.form['gender']
    cp=request.form['cp']
    trestbps=request.form['trestbps']
    chol=request.form['chol']
    fbs=request.form['fbs']
    restecg=request.form['restecg']
    thalach=request.form['thalach']
    exang=request.form['exang']
    oldpeak=request.form['oldpeak']
    slope=request.form['slope']
    ca=request.form['ca']
    thal=request.form['thal']
    if trestbps=='':
        trestbps=95
    if chol=='':
        chol=150
    if thalach=='':
        thalach=72
    if oldpeak=='':
        oldpeak=2

    recieved_features=[age, fgender, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak,slope,ca,thal]
    input_data={}
    input_data["age"]=age
    input_data["Gender"]=fgender
    input_data["Chest Pain Types"]=cp
    input_data["Resting Blood Pressure(in mm/Hg)"]=trestbps
    input_data["Cholesterol Level"]=chol
    input_data["is Fasting Blood Pressure>120mg/Dl?"]=fbs
    input_data["Resting Electro Cardio Graphic Result"]=restecg
    input_data["Maximum Heart Rate Achieved"]=thalach
    input_data["Does Exercise Induced Angina?"]=exang
    input_data["Old Peak (ST Depression Induced by Exercise Relative to Rest)"]=oldpeak
    input_data["Slope of ST Segment"]=slope
    input_data["number of major vessels (0-3) colored by flourosopy"]=ca
    input_data["Thal Type"]=thal



    if fgender=="Male":
        gender=1
    else:
        gender=0
    
    if thal=="Normal":
        thal=0
    elif thal=="Fixed Defect":
        thal=1
    else:
        thal=2

    # if cp=="Typical Angina":
    #     cp=0
    # elif cp=="Atypical Angina":
    #     cp=1
    # elif cp=="Non-Anginal":
    #     cp=2
    # else:
    #     cp=3
    # if fbs=="Yes":
    #     fbs=1
    # else:
    #     fbs=0
    if restecg=="Normal":
        restecg=0
    elif restecg=="STT Abnormality":
        restecg=1
    else:
        restecg=2
    if exang=="Yes":
        exang=1
    else:
        exang=0
    #  print("The email address is '" + age + "|"+sex+"|"+cp+"|"+trestbps+"|"+chol+"|"+fbs+"|"+restecg)
    # Get the data from the POST request.

    print("all models=",all_models)
    # print("Data recived", age, gender, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak,thal,0,0)
    age=int(age)
    cp=int(cp)
    trestbps=int(trestbps)
    chol=int(chol)
    fbs=int(fbs)
    thalach=int(thalach)
    oldpeak=int(oldpeak)
    slope=int(slope)
    ca=int(ca)
    features=[age, gender, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak,slope,ca,thal]
    print(features)
    dict={};
    avg=0
    for model in all_models:
        print("Model" , model)
        res=model.predict([features])
        print("res=",res[0],type(res))
        if res[0]==1:
            dict[model]="High Chance of Heart Disease"
        else:
            dict[model]="Low Chance of Heart Disease"
        avg+=res
    print("average=",type(avg))
    accuracy=avg[0]/5
    accuracy=round(accuracy,2)
    for result in dict:
        print("sfadgD", result)
    prediction = all_models[0].predict([features])

    # if(prediction[0]):
    #     return render_template('Hresult.html')
    # else:
    #     return render_template('Lresult.html')
    # if(prediction2[0]):
    #     output2 = "High Risk"
    # else:
    #     output2 = "Low Risk"
    personal_info=[name,email]
    responses=[input_data,dict,personal_info,accuracy]
    # Take the first value of prediction
    # output = prediction[0]
    # print("rESPONSES:",responses[0])
    return render_template("result.html",result = responses)
    


    
if __name__ == '__main__':
    app.run(port=5000, debug=True)


    