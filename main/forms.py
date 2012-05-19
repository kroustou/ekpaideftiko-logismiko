#-*- coding: utf-8 -*-
from django.contrib.auth.forms import UserCreationForm
from django import forms


class NewUserForm(UserCreationForm):
    first_name = forms.CharField(label=u'Όνομα')
    last_name = forms.CharField(label=u'Επώνυμο')
    is_staff = forms.BooleanField(required=False, label=u"Δάσκαλος", initial=False)

