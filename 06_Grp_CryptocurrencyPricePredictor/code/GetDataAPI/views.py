from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view

from GetDataAPI.serializers import CryptoPriceSerializer
from GetDataAPI.models import CryptoPrice


@api_view(['GET'])
def CryptoPriceViewSet(request):
   queryset = CryptoPrice.objects.all()
   serializer_class = CryptoPriceSerializer(queryset,many="True")
      # HttpResponse("Hello, world. You're at the polls testapi.")
   return Response(serializer_class.data)

def index(request):
    return render(request, 'index.html', {"college":"iet"})


def index1(request):
    return HttpResponse("Hello, world. You're at the polls index1.")
