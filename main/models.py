#-*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.forms.formsets import formset_factory
from django.core.validators import MaxValueValidator


DIFFICULTIES = (
		(u'1' , u'Εύκολο'),
		(u'2' , u'Μέτριο'),
		(u'3' , u'Δύσκολο'),
	)

CHOICES = (
		(u'True' , u'Σωστό'),
		(u'False' , u'Λάθος'),
	)


class Student(User):
	level = models.CharField(max_length=1 , choices=DIFFICULTIES)

class Example(models.Model):
 	chapterId = models.ForeignKey('Chapter')
	question = models.TextField()
	answer = models.TextField()

class Chapter(models.Model):
	title = models.CharField(max_length=120)
	content = models.TextField()
	difficulty = models.CharField(max_length=1 , choices=DIFFICULTIES)


class TrueOrFalse(models.Model):
    question = models.TextField(max_length=255)
    choices = models.CharField(max_length=255, choices=CHOICES)
    difficulty = models.CharField(max_length=1, choices=DIFFICULTIES)
    answer = models.CharField(max_length=255, choices=CHOICES)

    
class MultipleChoice(models.Model):
	question = models.CharField(max_length=255)
	choice1 = models.CharField(max_length=255)
	choice2 = models.CharField(max_length=255)
	choice3 = models.CharField(max_length=255)
	choice4 =  models.CharField(max_length=255)
	answer = models.PositiveIntegerField(validators=[MaxValueValidator(4)])
	difficulty = models.CharField(max_length=1, choices=DIFFICULTIES)


class FillTheBlanks(models.Model):
	question = models.TextField(max_length=255)
	answer = models.CharField(max_length=255)
	difficulty = models.CharField(max_length=1 , choices=DIFFICULTIES)


class Test(models.Model):
	difficulty = models.CharField(max_length=1 , choices=DIFFICULTIES)
	ex1 = models.ForeignKey('TrueOrFalse')
	ex2 = models.ForeignKey('MultipleChoice')
	ex3 = models.ForeignKey('FillTheBlanks')


class Examination(models.Model):
	test1 = models.ForeignKey('Test', related_name="+")
	test2 = models.ForeignKey('Test', related_name="+")
	test3 = models.ForeignKey('Test', related_name="+")
	difficulty = models.CharField(max_length=1 , choices=DIFFICULTIES)


class Grade(models.Model):
	student = models.ForeignKey('student')
	grade = models.PositiveIntegerField()
	difficulty = models.CharField(max_length=1 , choices=DIFFICULTIES)
