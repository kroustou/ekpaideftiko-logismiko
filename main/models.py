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

    def __unicode__(self):
        return u'%s' % (self.username)


class Example(models.Model):
    chapterId = models.ForeignKey('Chapter')
    question = models.TextField()
    answer = models.TextField()

    def __unicode__(self):
        return u'%s' % (self.question)


class Chapter(models.Model):
    title = models.CharField(max_length=120)
    contentEasy = models.TextField()
    contentMedium = models.TextField()
    contentHard = models.TextField()

    def __unicode__(self):
        return u'%s' % (self.title)


class Exercise(models.Model):
    chapterId = models.ForeignKey('Chapter', verbose_name=u'κεφάλαιο')
    difficulty = models.CharField(max_length=1, choices=DIFFICULTIES, verbose_name=u'δυσκολία')
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    exercise_type = generic.GenericForeignKey('content_type', 'object_id')

    def get_type(self):
        return self.exercise_type.__class__.__name__

    def __unicode__(self):
        return u'%s' % (self.exercise_type.question)


class TrueOrFalse(models.Model):
    question = models.CharField(max_length=255, verbose_name=u'Ερώτηση')
    answer = models.CharField(max_length=255, choices=CHOICES, verbose_name=u'Απάντηση')


class MultipleChoice(models.Model):
    choice1 = models.CharField(max_length=255, verbose_name=u'1')
    choice2 = models.CharField(max_length=255, verbose_name=u'2')
    choice3 = models.CharField(max_length=255, verbose_name=u'3')
    choice4 = models.CharField(max_length=255, verbose_name=u'4')
    question = models.CharField(max_length=255, verbose_name=u'Ερώτηση')
    answer = models.PositiveIntegerField(validators=[MaxValueValidator(4)], verbose_name=u'Σωστή απάντηση (1-4)')


class FillTheBlanks(models.Model):
    question = models.CharField(max_length=255, verbose_name=u'Ερώτηση')
    answer = models.CharField(max_length=255, verbose_name=u'Απάντηση')


class Test(models.Model):
    chapterId = models.ForeignKey('Chapter', verbose_name=u'κεφάλαιο')
    difficulty = models.CharField(max_length=1, choices=DIFFICULTIES)
    ex1 = models.ForeignKey('Exercise', related_name='+1')
    ex2 = models.ForeignKey('Exercise', related_name='+2')
    ex3 = models.ForeignKey('Exercise', related_name='+3')

    def __unicode__(self):
        return u'%s' % (self.ex1.exercise_type.question)


class Examination(models.Model):
    chapterId = models.ForeignKey('Chapter', verbose_name=u'κεφάλαιο')
    test1 = models.ForeignKey('Test', verbose_name=u'1ο θέμα', related_name="+")
    test1Score = models.PositiveIntegerField(verbose_name=u'μονάδες')
    test2 = models.ForeignKey('Test', verbose_name=u'2ο θέμα', related_name="+")
    test2Score = models.PositiveIntegerField(verbose_name=u'μονάδες')
    test3 = models.ForeignKey('Test', verbose_name=u'3ο θέμα', related_name="+")
    test3Score = models.PositiveIntegerField(verbose_name=u'μονάδες')
    availableTime = models.PositiveIntegerField()
    difficulty = models.CharField(max_length=1, choices=DIFFICULTIES)

    def __unicode__(self):
        return u'%s' % (self.test1.ex1.exercise_type.question)


class Mistakes(models.Model):
    student = models.ForeignKey('Student')
    exercise = models.ForeignKey('Exercise')
    timeMade = models.DateTimeField()
    answer = models.CharField(max_length=255)


class Grade(models.Model):
    student = models.ForeignKey('Student')
    exam = models.ForeignKey('Examination')
    takenOn = models.DateTimeField()
    grade = models.PositiveIntegerField()
