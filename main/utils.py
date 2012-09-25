from models import Exercise, Mistakes, Student
from datetime import datetime


def evaluate_answer(exercise_pk, answer, type, student):
    exercise = Exercise.objects.get(pk=exercise_pk)
    if (exercise.exercise_type.answer == answer):
        return True
    else:
        newMistake = Mistakes(student=student.student, exercise=exercise,
                              timeMade=datetime.now(), answer=answer)
        newMistake.save()
        return False
