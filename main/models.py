#-*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic


DIFFICULTIES = (
        (u'1', u'Εύκολο'),
        (u'2', u'Μέτριο'),
        (u'3', u'Δύσκολο'),
    )

CHOICES = (
        (u'True', u'Σωστό'),
        (u'False', u'Λάθος'),
    )


class Student(User):
    level = models.CharField(max_length=1, choices=DIFFICULTIES)


class Example(models.Model):
    chapterId = models.ForeignKey('Chapter')
    question = models.TextField()
    answer = models.TextField()


class Chapter(models.Model):
    title = models.CharField(max_length=120)
    contentEasy = models.TextField()
    contentMedium = models.TextField()
    contentHard = models.TextField()


class Exercise(models.Model):
    chapterId = models.ForeignKey('Chapter')
    difficulty = models.CharField(max_length=1, choices=DIFFICULTIES)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    exercise_type = generic.GenericForeignKey('content_type', 'object_id')

    def get_type(self):
        return self.exercise_type.__class__.__name__


class TrueOrFalse(models.Model):
    question = models.CharField(max_length=255)
    answer = models.CharField(max_length=255, choices=CHOICES)


class MultipleChoice(models.Model):
    choice1 = models.CharField(max_length=255)
    choice2 = models.CharField(max_length=255)
    choice3 = models.CharField(max_length=255)
    choice4 = models.CharField(max_length=255)
    question = models.CharField(max_length=255)
    answer = models.PositiveIntegerField(validators=[MaxValueValidator(4)])


class FillTheBlanks(models.Model):
    question = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)


class Test(models.Model):
    chapterId = models.ForeignKey('Chapter')
    difficulty = models.CharField(max_length=1, choices=DIFFICULTIES)
    ex1 = models.ForeignKey('Exercise', related_name='+1')
    ex2 = models.ForeignKey('Exercise', related_name='+2')
    ex3 = models.ForeignKey('Exercise', related_name='+3')


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
    student = models.ForeignKey('Student')
    exercise = models.ForeignKey('Exercise')
    timeMade = models.DateTimeField()
    answer = models.CharField(max_length=255)


class Grade(models.Model):
    student = models.ForeignKey('Student')
    exam = models.ForeignKey('Examination')
    takenOn = models.DateTimeField()
