#-*- coding: utf-8 -*-
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import ModelForm
from models import Example,Student, TrueOrFalse, FillTheBlanks, MultipleChoice, CHOICES, DIFFICULTIES, Test, Examination, Chapter, Exercise

EXERCISETYPES = (
        ('TrueOrFalse', 'Σωστό η Λάθος'),
        ('MultipleChoice', 'πολλαπλής επιλογής'),
        ('FillTheBlanks', 'συμπλήρωση κενού'),
    )


class NewUserForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Κωδικός")

    class Meta:
        model = Student
        fields = ('first_name', 'last_name', 'username', 'password')


class ExampleForm(ModelForm):
    form_type = forms.CharField(max_length=10, widget=forms.HiddenInput, initial='example')

    class Meta:
        model = Example

#Exercise Creation Forms#
#########################


class TrueOrFalseForm(ModelForm):
    form_type = forms.CharField(max_length=10, widget=forms.HiddenInput, initial='ToF')

    class Meta:
        model = TrueOrFalse


class FillTheBlanksForm(ModelForm):
    form_type = forms.CharField(max_length=3, widget=forms.HiddenInput, initial='FtB')

    class Meta:
        model = FillTheBlanks


class MultipleChoiceForm(ModelForm):
    form_type = forms.CharField(max_length=2, widget=forms.HiddenInput, initial='MC')

    class Meta:
        model = MultipleChoice

########################
########################


#Student Exercise Forms#
########################

class ExerciseForm(forms.ModelForm):
    exercise_type = forms.ChoiceField(label=u'Είδος άσκησης', choices=EXERCISETYPES)

    class Meta:
        model = Exercise
        fields = ('chapterId', 'difficulty')


class StudentTrueOrFalse(forms.Form):
    exercise_type = forms.CharField(max_length=10, widget=forms.HiddenInput, initial='ToF')
    answer = forms.ChoiceField(choices=CHOICES)


class StudentFillTheBlanks(forms.Form):
    exercise_type = forms.CharField(max_length=3, widget=forms.HiddenInput, initial='FtB')
    answer = forms.CharField(max_length=255)


class StudentMultipleChoice(forms.Form):
    exercise_type = forms.CharField(max_length=2, widget=forms.HiddenInput, initial='MC')
    answer = forms.ChoiceField(choices=[1, 2, 3, 4])

######################
######################


class SelectLevelForm(forms.Form):
    level = forms.ChoiceField(label=u'Επίπεδο',
                                choices=DIFFICULTIES)


class SelectChapterForm(forms.Form):
    chapter = forms.ModelChoiceField(queryset=Chapter.objects.all(), empty_label=None)


class TestForm(ModelForm):
    class Meta:
        model = Test


class ExamForm(ModelForm):
    class Meta:
        model = Examination
