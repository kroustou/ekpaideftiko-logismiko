#-*- coding: utf-8 -*-
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from forms import ExampleForm, NewUserForm, SelectLevelForm, TestForm, ExerciseForm, ExamForm, TrueOrFalseForm, FillTheBlanksForm, MultipleChoiceForm, StudentTrueOrFalse, StudentMultipleChoice, StudentFillTheBlanks
from django.views.decorators.csrf import csrf_exempt
from models import Example, Exercise, TrueOrFalse, MultipleChoice, FillTheBlanks, Mistakes
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
    return render_to_response('students/theory.html')

def example(request):
    examples = Example.objects.all()
    return  render_to_response('students/example.html',{'examples': examples})

@csrf_exempt
def add(request, type):
    message = ''
    template_name = 'professor/example.html'
    if type == 'example':
        form = ExampleForm(request.POST or None)
    elif type == 'test':
        form = TestForm(request.POST or None)
    elif type == 'exam':
        form = ExamForm(request.POST or None)
    elif type == 'exercise':
        form = ExerciseForm(request.POST or None)
        template_name = 'professor/exercise.html'
    if request.POST and form.is_valid: 
        form.save()
        message = "Αποθηκεύτηκε επιτυχώς!"
    return render_to_response(template_name, {'form': form, 'type': type, 'message': message})

def show_students(request):
    students = User.objects.filter(is_staff=False)
    return render_to_response('professor/students.html', {'students': students})

def test(request, test_type="exercise"):
    level = SelectLevelForm()
    return render_to_response('students/tests.html',{'level': level, 'type': test_type})

@csrf_exempt
def fetch(request):
    exercise_type = request.POST['exercise_type']
    if exercise_type == 'FillTheBlanks':
        print 'FillTheBlanks'
        form = FillTheBlanksForm()
    elif exercise_type == 'MultipleChoice':
        form = MultipleChoiceForm() 
    else:
        form = TrueOrFalseForm()
    return HttpResponse(str(form))
        
@csrf_exempt
def save(request):
    if request.POST:
        form_type = request.POST['form_type']
        if form_type == 'FtB':
            form = FillTheBlanksForm(request.POST)
        elif form_type == 'MC':
            form = MultipleChoiceForm(request.POST) 
        elif form_type == 'ToF':
            form = TrueOrFalseForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse_lazy('new-exercise'))
        else:
            return HttpResponse(str(form))
    else:
            return HttpResponse('Δεν θα έπρεπε να είστε εδώ!')

@csrf_exempt
def get_exercise(request):
    exercise_level = request.POST['exercise_level']
    type = random.choice([1, 2, 3])
    type =1
    if type == 1:
        exercise_set = FillTheBlanks.objects.filter(difficulty = exercise_level)
        form = StudentFillTheBlanks()
    elif type == 2:
        exercise_set = MultipleChoice.objects.filter(difficulty = exercise_level)
        form = StudentMultipleChoice()
    else:
        exercise_set = TrueOrFalse.objects.filter(difficulty = exercise_level)
        form = StudentTrueOrFalse
    print exercise_set
    exercise = random.choice(exercise_set)
    return render_to_response('students/exercise.html', {'type': type, 'exercise': exercise, 'form': form})

@csrf_exempt
def get_test(request):
    pass
    
@csrf_exempt
def get_exam(request):
    pass
 
@csrf_exempt
def evaluate_exercise(request):
    exercise_pk = request.POST['exercise_pk']
    answer = request.POST['answer']
    type = request.POST['exercise_type']
    print request.user.pk
    if(utils.evaluate_answer(exercise_pk=exercise_pk, answer=answer, type=type, student=request.user)):
        return HttpResponse('Right')
    else:
        return HttpResponse('Wrong')
        
@csrf_exempt
def evaluate_test(request):
    pass

@csrf_exempt
def evaluate_exam(request):
    pass
    