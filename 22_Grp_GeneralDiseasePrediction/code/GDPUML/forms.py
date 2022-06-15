from django import forms
from .models import Signup


class UserRegistration(forms.ModelForm):
    uemail = forms.EmailField(label='uemail')
    upass = forms.CharField(label='upass', max_length=50)
    uname = forms.CharField(label='uname', max_length=50)
    udate = forms.DateField(label='udate')

    class Meta:
        model = Signup
        fields = ('uname', 'uemail', 'upass', 'udate')
