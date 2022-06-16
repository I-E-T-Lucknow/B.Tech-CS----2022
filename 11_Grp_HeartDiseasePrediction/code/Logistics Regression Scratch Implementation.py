#!/usr/bin/env python
# coding: utf-8

# In[4]:


import numpy as np 
import pandas as pd
from numpy import log,dot,exp,shape
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification


# In[5]:


df = pd.read_csv("dataset/heart_data_set.csv")


# In[6]:


df.head()


# In[7]:


def standardize(X_tr):
    for i in range(shape(X_tr)[1]):
        X_tr[:,i] = (X_tr[:,i] - np.mean(X_tr[:,i]))/np.std(X_tr[:,i])
def F1_score(y,y_hat):
    tp,tn,fp,fn = 0,0,0,0
    for i in range(len(y)):
        if y[i] == 1 and y_hat[i] == 1:
            tp += 1
        elif y[i] == 1 and y_hat[i] == 0:
            fn += 1
        elif y[i] == 0 and y_hat[i] == 1:
            fp += 1
        elif y[i] == 0 and y_hat[i] == 0:
            tn += 1
    precision = tp/(tp+fp)
    recall = tp/(tp+fn)
    f1_score = 2*precision*recall/(precision+recall)
    return f1_score


# In[8]:


class LogidticRegression:
    def sigmoid(self,z):
        sig = 1/(1+exp(-z))
        return sig
    def initialize(self,X):
        weights = np.zeros((shape(X)[1]+1,1))
        X = np.c_[np.ones((shape(X)[0],1)),X]
        return weights,X
    def fit(self,X,y,alpha=0.001,iter=400):
        weights,X = self.initialize(X)
        def cost(theta):
            z = dot(X,theta)
            cost0 = y.T.dot(log(self.sigmoid(z)))
            cost1 = (1-y).T.dot(log(1-self.sigmoid(z)))
            cost = -((cost1 + cost0))/len(y)
            return cost
        cost_list = np.zeros(iter,)
        for i in range(iter):
            weights = weights - alpha*dot(X.T,self.sigmoid(dot(X,weights))-np.reshape(y,(len(y),1)))
            cost_list[i] = cost(weights)
        self.weights = weights
        return cost_list
    def predict(self,X):
        z = dot(self.initialize(X)[1],self.weights)
        lis = []
        for i in self.sigmoid(z):
            if i>0.5:
                lis.append(1)
            else:
                lis.append(0)
        return lis


# In[9]:


model = LogidticRegression()


# In[10]:


X_train = df.drop("target", axis = 1)
y_train = df["target"]


# In[11]:


X_train = X_train.to_numpy()
y_train = y_train.to_numpy()


# In[12]:


standardize(X_train)


# In[13]:


clf = model.fit(X_train, y_train)


# In[14]:


model.predict([[52, 1, 0, 125, 212, 0, 1, 168, 0, 1, 2, 2, 3]])


# In[15]:


out = model.predict(X_train)


# In[16]:


import pickle
import joblib


# In[17]:


from sklearn.metrics import accuracy_score


# In[18]:


accuracy_score(y_train, out)


# In[33]:


filename = 'logistic_regression_model.pkl'

joblib.dump(model, filename)
# In[35]:


loaded_model = joblib.load('logistic_regression_model.pkl')


# In[37]:


loaded_model.predict([[52, 1, 0, 125, 212, 0, 1, 168, 0, 1, 2, 2, 3]])


# In[ ]:





# In[ ]:





# In[ ]:




