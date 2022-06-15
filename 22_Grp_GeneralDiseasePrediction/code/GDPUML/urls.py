from django.urls import path
from .import views
urlpatterns=[
    path('',views.index,name='index'),
    path('dashBoard',views.dashBoard,name='dashBoard'),
    path('signup',views.signup,name='signup'),
    path('login',views.login,name='login'),
    path('predict_disease',views.predict_disease,name='pr'),
    path('prv',views.previous_disease,name='previous')


]