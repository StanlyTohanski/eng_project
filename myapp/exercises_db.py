from myapp.models import ExercisesDescriptions, ExercisesSentences


def get_exercises_list():
    exercises = []
    for item in ExercisesDescriptions.objects.all():
        exercises.append([item.exercise_id, item.exercise_name, item.exersise_description])
    return exercises


def get_exercise_data(exercise_id: int):
    tasks = []
    for item in ExercisesSentences.objects.filter(exercise_id__exact=exercise_id):
        sentence_parts = item.sentence.split('_')
        tasks.append({
            'task_id': item.sentence_id,
            '1st_part': sentence_parts[0],
            'user_input': '' if item.user_input is None else item.user_input,
            'prim_form': item.primitive_cut_part,
            '2nd_part': sentence_parts[1],
            'true_input': item.cut_part,
            'done': item.done == 1
            })
    return tasks


def get_exercise_info(exercise_id: int):
    for item in ExercisesDescriptions.objects.filter(exercise_id__exact=exercise_id):
        return [item.exercise_name, item.exersise_description]


def drop_result(exercise_id):
    for task in ExercisesSentences.objects.filter(exercise_id__exact=exercise_id):
        task.done = 0
        task.user_input = ''
        task.save()


def send_tasks(data_to_db):
    for user_task in data_to_db:
        task = ExercisesSentences.objects.get(sentence_id=user_task[0])
        task.done = 1 if task.cut_part.rstrip() == user_task[1].rstrip() else 0
        task.user_input = user_task[1]
        task.save()


def get_exercise_ids(exercise_id):
    tasks_id = []
    for item in ExercisesSentences.objects.filter(exercise_id__exact=exercise_id):
        tasks_id.append(item.sentence_id)
    return tasks_id


def get_stats():
    tasts_total = ExercisesSentences.objects.count()
    done_tasks_total = ExercisesSentences.objects.filter(done=1).count()

    exercises_ids = list(ExercisesDescriptions.objects.values_list('exercise_id').distinct())
    exercises_total = len(exercises_ids)
    done_exercises_total = 0
    for exercise_id in exercises_ids:
        ex_tasks_done = ExercisesSentences.objects.filter(exercise_id=exercise_id, done=1).count()
        ex_tasks_total = ExercisesSentences.objects.filter(exercise_id=exercise_id).count()
        if ex_tasks_done == ex_tasks_total:
            done_exercises_total += 1
    return tasts_total, done_tasks_total, exercises_total, done_exercises_total
