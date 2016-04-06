from django import forms
from news.models import *
from django.contrib.auth.models import User


class AddPageForm(forms.ModelForm):
    class Meta:
        model = News
        exclude = ('pub_date', 'update_date','views','auther')
        

class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username','password')