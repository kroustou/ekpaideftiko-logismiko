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
    contentEasy = models.TextField()
    contentMedium = models.TextField()
    contentHard = models.TextField()

#Cant see another way to store each students answers
class Exercise(models.Model):
    question = models.CharField(max_length=255)
    chapterId = models.ForeignKey('Chapter')
    difficulty = models.CharField(max_length=1, choices=DIFFICULTIES)

class TrueOrFalse(Exercise):
    answer = models.CharField(max_length=255, choices=CHOICES)

class MultipleChoice(Exercise):
    choice1 = models.CharField(max_length=255)
    choice2 = models.CharField(max_length=255)
    choice3 = models.CharField(max_length=255)
    choice4 =  models.CharField(max_length=255)
    answer = models.PositiveIntegerField(validators=[MaxValueValidator(4)])

class FillTheBlanks(Exercise):
    answer = models.CharField(max_length=255)

class Test(models.Model):
    chapterId = models.ForeignKey('Chapter')
    difficulty = models.CharField(max_length=1, choices=DIFFICULTIES)
    ex1 = models.ForeignKey('TrueOrFalse')
    ex2 = models.ForeignKey('MultipleChoice')
    ex3 = models.ForeignKey('FillTheBlanks')

class Examination(models.Model):
    chapterId = models.ForeignKey('Chapter')
    test1 = models.ForeignKey('Test', related_name="+")
    test1Score = models.PositiveIntegerField()
    test2 = models.ForeignKey('Test', related_name="+")
    test2Score = models.PositiveIntegerField()
    test3 = models.ForeignKey('Test', related_name="+")
    test3Score = models.PositiveIntegerField()
    availableTime = models.PositiveIntegerField()
    difficulty = models.CharField(max_length=1, choices=DIFFICULTIES)

class Mistakes(models.Model):
    student = models.ForeignKey('student')
    exercise = models.ForeignKey('Exercise')
    timeMade = models.DateTimeField()
    answer = models.CharField(max_length=255)

class Grade(models.Model):
    student = models.ForeignKey('Student')
    exam = models.ForeignKey('Examination')
    takenOn = models.DatetimeField() 
    