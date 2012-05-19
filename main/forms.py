#-*- coding: utf-8 -*-
from django.contrib.auth.forms import UserCreationForm
from django import forms


class NewUserForm(UserCreationForm):
    first_name = forms.CharField(label=u'Όνομα', help_text=u'το ονομά σας')
    last_name = forms.CharField(label=u'Επώνυμο', help_text=u'το επωνυμό σας')
    is_staff = forms.BooleanField(required=False, label=u"Δάσκαλος", initial=False, help_text=u'Είστε Δάσκαλος;')

