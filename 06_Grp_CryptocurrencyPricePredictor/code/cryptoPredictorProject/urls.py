"""cryptoPredictorProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from GetDataAPI import views
from mlmodel import CryptoModel
from GetDataAPI.models import CryptoPrice

def scriptt():
    CryptoPrice.objects.all().delete()
    CryptoModel('BTC').runmodel()
    CryptoModel('ETH').runmodel()
    # print(111111)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('test/', views.index, name='test'),
    path('test1/', views.index1, name='test1'),
    path('testAPI/', views.CryptoPriceViewSet, name='testAPI')
]

scriptt()
