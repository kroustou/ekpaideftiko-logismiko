#-*- coding: utf-8 -*-
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from forms import ExampleForm, NewUserForm, SelectLevelForm, TestForm, ExamForm, TrueOrFalseForm, FillTheBlanksForm, MultipleChoiceForm, StudentTrueOrFalse, StudentMultipleChoice, StudentFillTheBlanks, SelectChapterForm, ExerciseForm
from django.views.decorators.csrf import csrf_exempt
from models import Example, Exercise, Mistakes, Chapter, Test
from django.contrib.auth.models import User
import random
import utils


class RegistrationView(FormView):
    form_class = NewUserForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.set_password(form.cleaned_data['password'])
        obj.save()
        return super(RegistrationView, self).form_valid(self)


def main(request):
    user = request.user
    return render_to_response('front-page.html', {'user': user})


def theory(request):
    theory = Chapter.objects.all()
    return render_to_response('students/theory.html', {'chapters': theory})


def example(request):
    examples = Example.objects.all()
    return render_to_response('students/example.html', {'examples': examples})


@csrf_exempt
def add(request, type):
    message = ''
    commit = True
    template_name = 'professor/example.html'
    if type == 'example':
        form = ExampleForm(request.POST or None)
    elif type == 'test':
        form = TestForm(request.POST or None)
    elif type == 'exam':
        form = ExamForm(request.POST or None)
    elif type == 'exercise':
        commit = False
        form = ExerciseForm()
        if request.POST:
            subform = eval(request.POST['exercise_type'] + 'Form(request.POST)')
            if subform.is_valid():
                obj = subform.save(commit=False)
            form = ExerciseForm(request.POST)
            if form.is_valid():
                exercise_object = form.save(commit=False)
                obj.save()
                exercise_object.exercise_type = obj
                exercise_object.save()
        template_name = 'professor/exercise.html'
    if request.POST and form.is_valid and commit:
        form.save()
    elif not commit:
        message = "Αποθηκεύτηκε επιτυχώς!"
    return render_to_response(template_name, {'form': form, 'type': type, 'message': message})


def show_students(request):
    students = User.objects.filter(is_staff=False)
    return render_to_response('professor/students.html', {'students': students})


def test(request, test_type="exercise"):
    level = SelectLevelForm()
    chapter = SelectChapterForm()
    return render_to_response('students/tests.html', {'level': level, 'chapter': chapter, 'type': test_type})


@csrf_exempt
def fetch(request):
    exercise_type = request.POST['exercise_type']
    print exercise_type
    if exercise_type == 'FillTheBlanks':
        form = FillTheBlanksForm()
    elif exercise_type == 'MultipleChoice':
        form = MultipleChoiceForm()
    else:
        form = TrueOrFalseForm()
    return HttpResponse(str(form))


@csrf_exempt
def get_exercise(request):
    exercise_level = request.POST['exercise_level']
    chapter = int(request.POST['chapter']) - 1
    exercise = Exercise.objects.filter(chapterId=chapter, difficulty=exercise_level)
    if exercise:
        exercise = random.choice(list(exercise))
        return render_to_response('students/exercise.html', {'exercise': exercise})
    else:
        return HttpResponse(u'Δεν βρέθηκαν ασκήσεις')


@csrf_exempt
def get_test(request):
    test_level = request.POST['test_level']
    chapter = int(request.POST['chapter']) - 1
    test = Test.objects.filter(chapterId=chapter, difficulty=test_level)
    if test:
        test = random.choice(list(test))
        return render_to_response('students/test.html', {'test': test})
    else:
        return HttpResponse(u'Δεν βρέθηκαν τέστ')


@csrf_exempt
def get_exam(request):
    pass


@csrf_exempt
def evaluate_exercise(request):
    exercise_pk = request.POST['exercise_pk']
    answer = request.POST['answer']
    print answer
    print request.user.pk
    if (utils.evaluate_answer(exercise_pk=exercise_pk, answer=answer, type=type, student=request.user)):
        return HttpResponse('Right')
    else:
        return HttpResponse('Wrong')


@csrf_exempt
def evaluate_test(request):
    pass


@csrf_exempt
def evaluate_exam(request):
    pass
