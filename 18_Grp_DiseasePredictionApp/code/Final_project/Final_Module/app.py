from flask import Flask,render_template,request,session, url_for, redirect,flash 
#from flask_mysqldb import MySQL
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
#from sklearn import datasets
import pickle
import pymysql
import pandas as pd
global to_scale
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
from werkzeug.utils import secure_filename
import os
from tensorflow import keras
import cv2
from tensorflow.keras.preprocessing import image
import numpy as np


def dbConnection():
    connection = pymysql.connect(host="localhost", user="root", password="root", database="creditcard155")
    return connection

def dbClose():
    dbConnection().close()    
    return

app=Flask(__name__)
app.secret_key = 'random string'
UPLOAD_FOLDER = 'static/uploadedimages'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home.html')
def home():
    return render_template('home.html')

@app.route('/logout')
def logout():
    session.pop('user')
    session.pop('userid')
    return render_template('home.html')

@app.route('/register',methods=['POST','GET'] )
def register():
    if request.method == "POST":
        try:
            status=""
            fname = request.form.get("name")
            add = request.form.get("add")
            pno = request.form.get("pno")
            email = request.form.get("email")
            pass1 =  request.form.get("pass1")
            con = dbConnection()
            cursor = con.cursor()
            cursor.execute('SELECT * FROM userdetailes WHERE email = %s', (email))
            res = cursor.fetchone()
            #res = 0
            if not res:
                sql = "insert into userdetailes (name, address,phone,email,password) VALUES (%s,%s, %s, %s, %s)"
                val = (fname ,add ,pno ,email ,pass1)
                print(sql," ",val)
                cursor.execute(sql, val)
                con.commit()
                status= "success"
                return render_template("login.html")
            else:
                status = "Already available"
            #return status
            return redirect(url_for('index'))
        except Exception as e:
            print(e)
            print("Exception occured at user registration")
            return redirect(url_for('index'))
        finally:
            dbClose()
    return render_template('register.html')


@app.route('/login',methods=['POST','GET'])
def login():
    msg = ''
    if request.method == "POST":
        session.pop('user',None)
        mailid = request.form.get("email")
        password = request.form.get("pass1")
        #print(mobno+password)
        con = dbConnection()
        cursor = con.cursor()
        result_count = cursor.execute('SELECT * FROM userdetailes WHERE email = %s AND password = %s', (mailid, password))
        #a= 'SELECT * FROM userdetails WHERE mobile ='+mobno+'  AND password = '+ password
        print(result_count)
        #result_count=cursor.execute(a)
        result = cursor.fetchone()
        if result_count>0:
            print(result_count)
            session['user'] = mailid
            session['userid']= result[0]
            return render_template("home.html")
        else:
            print(result_count)
            msg = 'Incorrect username/password!'
            return msg
    return render_template('login.html')

@app.route('/diabeties',methods=['POST','GET'])
def diabeties():
    if request.method == "POST":
    
        dict = {'age':request.form.get("age"),
                   'Gender':request.form.get("Gender"),
                   'Polyuria':request.form.get("Polyuria"),
                   'Polydipsia':request.form.get("Polydipsia"),
                   'weight':request.form.get("weight"),
                   'Weekness':request.form.get("Weekness"),
                   'Polyphagia':request.form.get("Polyphagia"),
                   'thrush':request.form.get("thrush"),
                   'blurring':request.form.get("blurring"),
                   'Itching':request.form.get("Itching"),
                   'Irritability':request.form.get("Irritability"),
                   'healing':request.form.get("healing"),
                   'paresis':request.form.get("paresis"),
                   'stiffness':request.form.get("stiffness"),
                   'Alopecia':request.form.get("Alopecia"),
                   'Obesity':request.form.get("Obesity")}
        df=pd.DataFrame(dict,index=[0])
        print(df)

        with open("diabeties_models/rfc_pickle",'rb') as f:
            st=pickle.load(f)
        ed=st.predict(df)
        print("printing prediction")
        print(ed)  
        if ed[0]==1:
           flash("You might have Diabeties. Please consult with doctores.")
        else: 
            flash("You don't have Diabetis. Please consult with Doctor for verification.")
    return render_template('diabeties.html')
    
@app.route("/skin",methods=['POST','GET'])
def newvalidate():
    print("hii before post")
    if request.method=="POST":
        print("hii after post")
        f1 = request.files['file1']
        print("f1")
        print(f1)

        filename = secure_filename(f1.filename)
        print(filename)
        f1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        img = cv2.imread("static/uploadedimages/"+str(filename))
        
        image_size=224
        #img = cv2.imread(path1+"//"+i)
        path="static/uploadedimages/"+"//"+str(filename)
        img = image.load_img(path, target_size=(image_size, image_size))
        x = image.img_to_array(img)
        print(type(x))
        img_4d=x.reshape(1,224,224,3)
        #img_4d=img_4d/255
        model = keras.models.load_model('skin_models/VGGSKin_8classes.hp5')
        #predictions = model.predict(img_4d)
       # print(predictions)
        predictions = model.predict(img_4d)
        print(predictions)
        pred=np.argmax(predictions[0])
        print(pred)
        #a=list(predictions[0]).index(max(predictions[0]))
        #print(a)
        dict1=['acne',
         'Clear_Skin',
         'hairloss',
         'melanoma',
         'nailfungus',
         'Poison Ivy Photos and other Contact Dermatitis',
         'vitiligo',
         'Warts Molluscum and other Viral Infections']
        a=dict1[pred]
        #list1=['adenocarcinoma_left.lower.lobe_T2_N0_M0_Ib','large.cell.carcinoma_left.hilum_T2_N2_M0_IIIa','squamous.cell.carcinoma_left.hilum_T1_N2_M0_IIIa']
        flash(str(a)+" Detected in Image")
       
    return render_template("skin.html")


if __name__=="__main__":
    app.run("0.0.0.0")
    # app.run(debug=True)