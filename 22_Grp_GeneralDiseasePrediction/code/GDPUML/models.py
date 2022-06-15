from django.db import models


# Create your models here.
class Signup(models.Model):
    uname = models.CharField(max_length=50)
    uemail = models.EmailField()
    upass = models.CharField(max_length=50)
    udate=models.DateField()

class Login(models.Model):
    uemail = models.EmailField()
    upass = models.CharField( max_length=50)

class GetPrediction(models.Model):
    uname=models.CharField(max_length=100)
    s1=models.CharField(max_length=100)
    s2 = models.CharField(max_length=100)
    s3 = models.CharField(max_length=100)
    s4 = models.CharField(max_length=100)
    s5 = models.CharField(max_length=100)
    p1 = models.CharField(max_length=100)
    p2 = models.CharField(max_length=100)
    p3 = models.CharField(max_length=100)
    date1 = models.CharField(max_length=100)

