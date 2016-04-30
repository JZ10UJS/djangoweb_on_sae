# coding: utf-8
from django import forms
from news.models import *
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
import re


class AddPageForm(forms.Form):
    CHOICE = (
        ('HX', u'虎嗅'),
    )
    info_from = forms.ChoiceField(choices=CHOICE)
    info_nums = forms.IntegerField(initial=10)

        

class RegisterForm(forms.ModelForm):
    error_css_class = 'danger'
    password = forms.CharField(widget=forms.PasswordInput())
    
    def clean_username(self):
        uname = self.cleaned_data['username']
        if not re.match(r'[_a-zA-Z][a-zA-Z0-9]{7,19}', uname):
            raise forms.ValidationError(u'用户名以字母或下划线开头，8-20位！')
        return uname
    class Meta:
        model = User
        fields = ('username','password')
        help_texts = {'username':_(u'用户名以字母或下划线开头，8-20位！'),}