#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Basic
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
print("successful import ;)")


# In[2]:


from matplotlib import rcParams
from matplotlib.cm import rainbow
print("success")


# In[3]:


get_ipython().run_line_magic('matplotlib', 'inline')
import warnings
warnings.filterwarnings('ignore')
print("success")


# In[4]:


# Other libraries
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn import *
print("success")


# In[5]:


from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
print("success")


# In[6]:


heartData=pd.read_csv("./dataset/heart_data_set.csv");
heartData.info()
heartData.describe()


# In[7]:


rcParams['figure.figsize'] = 10,10
plt.matshow(heartData.corr())
plt.yticks(np.arange(heartData.shape[1]), heartData.columns)
plt.xticks(np.arange(heartData.shape[1]), heartData.columns)
plt.colorbar()


# In[8]:


corr = heartData.corr()

corr.style.background_gradient(cmap='coolwarm')


# In[9]:


rcParams['figure.figsize'] = 8,6
plt.bar(heartData['target'].unique(), heartData['target'].value_counts(), color = ['black', 'silver'])
plt.xticks([0, 1])
plt.xlabel('Target Classes')
plt.ylabel('Count')
plt.title('Count of each Target Class')


# In[10]:



X = heartData.drop(['target'], axis = 1)
y = heartData['target']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.70, random_state = 0)
print(X_train.shape[0],X_test.shape[0], y_train.shape[0], y_test.shape[0])


# In[11]:


#dated::10/04/2022
knn_scores = []
for k in range(2,21):
    knn_classifier = KNeighborsClassifier(n_neighbors = k)
    knn_classifier.fit(X_train, y_train)
    knn_score=round(knn_classifier.score(X_test, y_test),2)
    knn_scores.append(knn_score)


knn_classifier = KNeighborsClassifier(n_neighbors = 5)
knn_classifier.fit(X_train, y_train)
knn_score=knn_classifier.predict(X_test)
print(accuracy_score(y_test,knn_score))


# In[12]:


plt.plot([k for k in range(2, 21)], knn_scores, color = 'red')
for i in range(2,21):
    plt.text(i, knn_scores[i-2], (i, knn_scores[i-2]))
plt.xticks([i for i in range(2, 21)])
plt.xlabel('Number of Neighbors (K)')
plt.ylabel('Scores')
plt.title('KNN Scores for different K neighbouras')


# In[13]:


# SVM NOW dated::20/04/2022

from sklearn.metrics import accuracy_score

svc_scores = []
kernels = ['linear', 'poly', 'rbf', 'sigmoid']
for i in range(len(kernels)):
    svc_classifier = SVC(kernel = kernels[i])
    svc_classifier.fit(X_train, y_train)
    svc_scores.append(round(svc_classifier.score(X_test, y_test),2))

svc_classifier = SVC(kernel = kernels[0])
svc_classifier.fit(X_train, y_train)
svc_prediction_result=svc_classifier.predict(X_test)
#print(svc_prediction_result)
print(accuracy_score(y_test,svc_prediction_result))


# In[14]:



colors = rainbow(np.linspace(0, 1, len(kernels)))
plt.bar(kernels, svc_scores, color = colors)
for i in range(len(kernels)):
    plt.text(i, svc_scores[i], svc_scores[i])
plt.xlabel('Kernels')
plt.ylabel('Scores')
plt.title('SVM scores Activation function wise...')


# In[ ]:





# In[15]:


print(knn_scores)
print(max(knn_scores))


# In[16]:


knn_classifier = KNeighborsClassifier(n_neighbors = 3)
knn_classifier.fit(X_train, y_train)
check_data1 = np.array([[52,1,0,125,212,0,1,168,0,1,2,2,3]])
prediction_result = knn_classifier.predict(check_data1)
print("Prediction: {}".format(prediction_result))


# In[17]:


# print(classifiction_report(y_test)


# In[18]:


dt_scores = []
for i in range(1, len(X.columns) + 1):
    dt_classifier = DecisionTreeClassifier(max_features = i, random_state = 0)
    dt_classifier.fit(X_train, y_train)
    dt_scores.append(round(dt_classifier.score(X_test, y_test),2))
print("Done")


# In[19]:


print(dt_scores)


# In[20]:


plt.plot([i for i in range(1, len(X.columns) + 1)], dt_scores, color = 'green')
for i in range(1, len(X.columns) + 1):
    plt.text(i, dt_scores[i-1], (i, dt_scores[i-1]))
plt.xticks([i for i in range(1, len(X.columns) + 1)])
plt.xlabel('Max features')
plt.ylabel('Scores')
plt.title('Decision Tree Classifier scores for different number of maximum features')


# In[21]:



rf_scores = []
estimators = [10, 20,100, 200, 500]
for i in estimators:
    rf_classifier = RandomForestClassifier(n_estimators = i, random_state = 0)
    rf_classifier.fit(X_train, y_train)
    rf_scores.append(round(rf_classifier.score(X_test, y_test),2))


# In[22]:


colors = rainbow(np.linspace(0, 1, len(estimators)))
plt.bar([i for i in range(len(estimators))], rf_scores, color = colors, width = 0.8)
for i in range(len(estimators)):
    plt.text(i, rf_scores[i], rf_scores[i])
plt.xticks(ticks = [i for i in range(len(estimators))], labels = [str(estimator) for estimator in estimators])
plt.xlabel('Number of estimators')
plt.ylabel('Scores')
plt.title('Random Forest Classifier scores for different number of estimators')


# In[23]:


rf_model = RandomForestClassifier(n_estimators = 20, random_state = 0)
rf_model.fit(X_train, y_train)
rf_model_result=rf_classifier.predict(X_test)
print(accuracy_score(y_test,rf_model_result))


# In[24]:


logistic_model = LogisticRegression()
logistic_model.fit(X_train, y_train)
logistic_model_prediction=logistic_model.predict(X_test)
print(accuracy_score(y_test,logistic_model_prediction))
print(classification_report(y_test,logistic_model_prediction))


# In[25]:


dt_classifier = DecisionTreeClassifier(max_features = 13, random_state = 0)
dt_classifier.fit(X_train, y_train)


# In[28]:


import pickle
all_models=[rf_classifier,logistic_model,dt_classifier,svc_classifier,knn_classifier]
#pickle.dump(logistic_model,open("models.pkl","wb"))
#pickle.dump(rf_classifier,open("models.pkl","wb"))
with open("models.pkl", 'wb') as files:
    pickle.dump(all_models, files)
print("Done")


# In[29]:


open_file = open("models.pkl", "rb")
loaded_list = pickle.load(open_file)
print(loaded_list)
open_file.close()
print("Done")



