#-*- coding: utf-8 -*-
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from forms import ExampleForm, NewUserForm, SelectLevelForm, TestForm, ExamForm, TrueOrFalseForm, FillTheBlanksForm, MultipleChoiceForm, StudentTrueOrFalse, StudentMultipleChoice, StudentFillTheBlanks, SelectChapterForm, ExerciseForm
from django.views.decorators.csrf import csrf_exempt
from models import Student, Example, Exercise, Mistakes, Chapter, Test, Examination as Exam, Grade, Mistakes
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
    if user.is_staff:
        return show_students(request)
    else:
        return theory(request)


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
    exam_level = request.POST['exam_level']
    chapter = int(request.POST['chapter']) - 1
    exam = Exam.objects.filter(chapterId=chapter, difficulty=exam_level)
    if exam:
        exam = random.choice(list(exam))
        return render_to_response('students/exam.html', {'exam': exam})
    else:
        return HttpResponse(u'Δεν βρέθηκαν διαγωνίσματα')


@csrf_exempt
def evaluate_exercise(request):
    exercise_pk = request.POST['exercise_pk']
    answer = request.POST['answer']
    if (utils.evaluate_answer(exercise_pk=exercise_pk, answer=answer, type=type, student=request.user)):
        msg = u'Σωστά!'
    else:
        msg = u'Λάθος!'
    return render_to_response('student.html', {'message': msg})


@csrf_exempt
def evaluate_test(request):
    test_pk = request.POST['test_pk']
    answer1 = request.POST['answer-ex1']
    answer2 = request.POST['answer-ex2']
    answer3 = request.POST['answer-ex3']
    result = utils.evaluate_test(test_pk=test_pk, answers=[answer1, answer2, answer3], type=type, student=request.user)
    msg = 'right answers:' + str(result)
    return render_to_response('student.html', {'message': msg})


@csrf_exempt
def evaluate_exam(request):
    exam_pk = request.POST['exam_pk']
    answers = []
    if 'answer-test1-ex1' in request.POST:
        answers.append(request.POST['answer-test1-ex1'])
    else:
        answers.append("")
    if 'answer-test1-ex2' in request.POST:
        answers.append(request.POST['answer-test1-ex2'])
    else:
        answers.append("")
    if 'answer-test1-ex3' in request.POST:
        answers.append(request.POST['answer-test1-ex3'])
    else:
        answers.append("")
    if 'answer-test2-ex1' in request.POST:
        answers.append(request.POST['answer-test2-ex1'])
    else:
        answers.append("")
    if 'answer-test2-ex2' in request.POST:
        answers.append(request.POST['answer-test2-ex2'])
    else:
        answers.append("")
    if 'answer-test2-ex3' in request.POST:
        answers.append(request.POST['answer-test2-ex3'])
    else:
        answers.append("")
    if 'answer-test3-ex1' in request.POST:
        answers.append(request.POST['answer-test3-ex1'])
    else:
        answers.append("")
    if 'answer-test3-ex2' in request.POST:
        answers.append(request.POST['answer-test3-ex2'])
    else:
        answers.append("")
    if 'answer-test3-ex3' in request.POST:
        answers.append(request.POST['answer-test3-ex3'])
    else:
        answers.append("")
    result = utils.evaluate_exam(exam_pk=exam_pk, answers=answers, type=type, student=request.user)
    msg = 'Ο βαθμός σου:' + str(result)
    return render_to_response('student.html', {'message': msg})


def progress(request):
    grades = Grade.objects.filter(student=request.user).prefetch_related()
    mistakes = Mistakes.objects.filter(student=request.user).prefetch_related()
    return render_to_response('students/progress.html', {'grades': grades, 'mistakes': mistakes})


def students_progress(request):
    grades = Grade.objects.all().prefetch_related()
    return render_to_response('professor/progress.html', {'grades': grades})


@csrf_exempt
def change_student(request):
    student = Student.objects.get(pk=request.POST['id']);
    student.first_name = request.POST['name'];
    student.last_name= request.POST['last_name'];
    student.save()
    return HttpResponse('done')