from django.shortcuts import render
from django.core.cache import cache

from myapp import exercises_db
from myapp import feedback_save


def index(request):
    return render(request, "index.html")


def exercises_list(request):
    exercises = exercises_db.get_exercises_list()
    return render(request, "exercises_list.html", context={"exercises": exercises})


def exercise(request, exercise_id: int):
    exercise_name, exercise_description = exercises_db.get_exercise_info(exercise_id)
    submit = 0
    if request.method == "POST":
        cache.clear()
        data_to_db = []
        for key in list(request.POST.keys())[1:]:
            task_id = int(key[11:])
            user_input = request.POST.get(key)
            data_to_db.append([task_id, user_input])
        exercises_db.send_tasks(data_to_db)
        submit = 1

    tasks = exercises_db.get_exercise_data(exercise_id)
    cur_context = {'tasks': tasks,
                   'exercise_id': exercise_id,
                   'exercise_name': exercise_name,
                   'exercise_description': exercise_description,
                   'submit': submit,
                   }
    return render(request, "exercise.html", context=cur_context)


def exercise_drop(request, exercise_id: int):
    exercises_db.drop_result(exercise_id)
    exercise_name, exercise_description = exercises_db.get_exercise_info(exercise_id)
    submit = 0
    tasks = exercises_db.get_exercise_data(exercise_id)
    cur_context = {'tasks': tasks,
                   'exercise_id': exercise_id,
                   'exercise_name': exercise_name,
                   'exercise_description': exercise_description,
                   'submit': submit
                   }
    return render(request, "exercise.html", context=cur_context)


def feedback(request):
    return render(request, "feedback.html")


def send_feedback(request):
    if request.method == "POST":
        cache.clear()
        user_name = request.POST.get("name")
        email = request.POST.get("email", "")
        email = email if len(email) != 0 else None
        fb_text = request.POST.get("fb_text", "").replace(";", ",")
        context = {"user": user_name}
        if len(fb_text) == 0:
            context["success"] = False
            context["comment"] = "Поле для отзыва должно быть не пустым"
        else:
            context["success"] = True
            context["success-title"] = ""
            context["comment"] = "Ваш отзыв отправлен"
            feedback_save.save_fb(user_name, email, fb_text)
        # if context["success"]:
        #     context["success-title"] = ""
        return render(request, "feedback_request.html", context)
    feedback(request)


def show_stats(request):
    tasts_total, done_tasks_total, exercises_total, done_exercises_total = exercises_db.get_stats()
    return render(request, "stats.html", {'tasts_total': tasts_total,
                                          'done_tasks_total': done_tasks_total,
                                          'exercises_total': exercises_total,
                                          'done_exercises_total': done_exercises_total})
