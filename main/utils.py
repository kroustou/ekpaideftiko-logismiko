from models import Exercise, Mistakes, Test, Examination, Grade
from datetime import datetime


def evaluate_answer(exercise_pk, answer, type, student):
    exercise = Exercise.objects.get(pk=exercise_pk)
    if (str(exercise.exercise_type.answer) == str(answer)):
        return True
    else:
        newMistake = Mistakes(student=student.student, exercise=exercise,
                              timeMade=datetime.now(), answer=answer)
        newMistake.save()
        return False


def evaluate_test(test_pk, answers, type, student):
    test = Test.objects.get(pk=test_pk)
    right = 0
    if str(test.ex1.exercise_type.answer) == str(answers[0]):
        right += 1
    else:
        newMistake = Mistakes(student=student.student, exercise=test.ex1,
                              timeMade=datetime.now(), answer=answers[0])
        newMistake.save()
    if str(test.ex2.exercise_type.answer) == str(answers[1]):
        right += 1
    else:
        newMistake = Mistakes(student=student.student, exercise=test.ex2,
                              timeMade=datetime.now(), answer=answers[1])
        newMistake.save()
    if str(test.ex3.exercise_type.answer) == str(answers[2]):
        right += 1
    else:
        newMistake = Mistakes(student=student.student, exercise=test.ex3,
                              timeMade=datetime.now(), answer=answers[2])
        newMistake.save()
    return right


def evaluate_exam(exam_pk, answers, type, student):
    exam = Examination.objects.get(pk=exam_pk)
    grade = 0

    rights = evaluate_test(exam.test1.id, answers[:3], type=type, student=student)
    grade = rights * exam.test1Score / 3

    rights = evaluate_test(exam.test2.id, answers[3:6], type=type, student=student)
    grade += rights * exam.test2Score / 3

    rights = evaluate_test(exam.test3.id, answers[6:], type=type, student=student)
    grade += rights * exam.test2Score / 3

    newGrade = Grade(student=student.student, exam=exam, takenOn=datetime.now(), grade=grade)
    newGrade.save()
    return grade
