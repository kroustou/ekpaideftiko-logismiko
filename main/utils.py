def evaluate_answer(exercise_pk, answer):
    exercise = Exercise.objects.get(pk = exercise_pk)
    if (exercise.answer == answer):
        return True
    else:
        newMistake = Mistakes(student=request.user , exercise=exercise_pk, 
                              timeMade=datetime.now(), answer=answer )
        newMistake.save()
        return False