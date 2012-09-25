from models import Exercise, FillTheBlanks, MultipleChoice, Mistakes, Student
from datetime import datetime

def evaluate_answer(exercise_pk, answer, type, student):
    if (type == 'ToF'):
        exercise = TrueOrFalse.objects.get(pk = exercise_pk)
    elif(type == 'FtB'):
        exercise = FillTheBlanks.objects.get(pk = exercise_pk)
    else:
        exercise = MultipleChoice.objects.get(pk = exercise_pk)
    if (exercise.answer == answer):
        return True
    else:
        newMistake = Mistakes(student=student.student , exercise=exercise, 
                              timeMade=datetime.now(), answer=answer )
        newMistake.save()
        return False