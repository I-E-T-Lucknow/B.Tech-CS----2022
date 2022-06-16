from rest_framework import serializers
from GetDataAPI.models import CryptoPrice

class CryptoPriceSerializer(serializers.ModelSerializer):
   class Meta:
       model = CryptoPrice
       fields = ('date', 'value', 'flag')