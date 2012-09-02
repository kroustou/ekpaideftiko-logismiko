#-*- coding: utf-8 -*-
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import ModelForm

from models import Example,Student, TrueOrFalse, FillTheBlanks, MultipleChoice, DIFFICULTIES, Test, Examination

EXERCISETYPES = (
		('TrueOrFalse', 'Σωστό η Λάθος'),
		('MultipleChoice', 'πολλαπλής επιλογής'),
		('FillTheBlanks', 'συμπλήρωση κενού'),
	)

class NewUserForm(ModelForm):
	password = forms.CharField( widget=forms.PasswordInput, label="Κωδικός" )
	class Meta:
		model = Student
		fields = ('first_name', 'last_name', 'username', 'password')


class ExampleForm(ModelForm):
	form_type = forms.CharField(max_length=10, widget=forms.HiddenInput, initial='example')
	class Meta:
		model = Example


class TrueOrFalse(ModelForm):
	form_type = forms.CharField(max_length=10, widget=forms.HiddenInput, initial='ToF')
	class Meta:
		model = TrueOrFalse


class FillTheBlanks(ModelForm):
	form_type = forms.CharField(max_length=3, widget=forms.HiddenInput, initial='FtB')
	class Meta:
		model = FillTheBlanks

class MultipleChoice(ModelForm):
	form_type = forms.CharField(max_length=2, widget=forms.HiddenInput, initial='MC')
	class Meta:
		model = MultipleChoice

class SelectLevelForm(forms.Form):
	level = forms.ChoiceField(label=u'Επίπεδο',
								choices=DIFFICULTIES)

class TestForm(ModelForm):
	class Meta:
		model = Test

class ExamForm(ModelForm):
	class Meta:
		model = Examination

class ExerciseForm(forms.Form):
	exercise_type = forms.ChoiceField(label=u'Είδος άσκησης',
								choices=EXERCISETYPES)

