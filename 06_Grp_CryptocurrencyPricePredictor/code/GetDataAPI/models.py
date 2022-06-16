from django.db import models

class CryptoPrice(models.Model):
	date = models.DateTimeField()
	value = models.BigIntegerField()
	flag = models.IntegerField()