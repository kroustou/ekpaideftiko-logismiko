#-*- coding: utf-8 -*-
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from forms import ExampleForm, NewUserForm, SelectLevelForm, TestForm, ExerciseForm, ExamForm, TrueOrFalse, FillTheBlanks, MultipleChoice
from django.views.decorators.csrf import csrf_exempt
from models import Example
from django.contrib.auth.models import User

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
        form = FillTheBlanks()
    elif exercise_type == 'MultipleChoice':
        form = MultipleChoice() 
    else:
        form = TrueOrFalse()
    return HttpResponse(str(form))
        
@csrf_exempt
def save(request):
    if request.POST:
        form_type = request.POST['form_type']
        if form_type == 'FtB':
            form = FillTheBlanks(request.POST)
        elif form_type == 'MC':
            form = MultipleChoice(request.POST) 
        elif form_type == 'ToF':
            form = TrueOrFalse(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse_lazy('new-exercise'))
        else:
            return HttpResponse(str(form))
    else:
            return HttpResponse('Δεν θα έπρεπε να είστε εδώ!')
