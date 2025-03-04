import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from .models import StageSevenProgress
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from .forms import RegisterUserForm, LoginForm
from .models import QuizResult


def register(request):
    if request.method == 'POST':
        user_form = RegisterUserForm(request.POST)

        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password1'])
            new_user.save()
            return redirect('login')  # Перенаправление на страницу входа
        else:
            return render(request, 'accounts/register.html', {'form': user_form})
    else:
        user_form = RegisterUserForm()
        return render(request, 'accounts/register.html', {'form': user_form})


def user_login(request):
    # root, root
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('seven_levels')
            else:
                form.add_error(None, "Неверное имя пользователя или пароль")
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')  # После выхода перенаправляем на страницу входа


def presentation(request):
    return render(request, 'accounts/presentation_first.html')


def sec_page(request):
    return render(request, 'accounts/presentation_sec.html')


def seven_levels(request):
    return render(request, 'accounts/seven_levels.html')


@login_required
def map(request):
    usr = request.user
    # Получаем результаты этапов 1–6 из QuizResult
    all_results = QuizResult.objects.filter(user=usr)
    all_results_sorted = sorted(all_results, key=lambda x: x.step)

    # Создаём список наград для этапов 1–6
    total_stages = 6  # Учитываем только этапы 1–6
    awards = []
    for step in range(1, total_stages + 1):
        completed = False
        for stat in all_results_sorted:
            if stat.step == step:
                # Проверяем, что все задания выполнены (score == total_questions)
                # Если total_questions не задано, проверяем score == 1
                if stat.total_questions:
                    completed = stat.score == stat.total_questions
                else:
                    completed = stat.score == 1
                break
        awards.append({'step': step, 'completed': completed})

    # Получаем данные о 7-м этапе из StageSevenProgress
    stage_seven_progress = StageSevenProgress.objects.filter(user=usr).first()
    stage_seven_completed = False
    if stage_seven_progress:
        # Проверяем, все ли задания 7-го этапа выполнены
        stage_seven_completed = (
            stage_seven_progress.badge_initiation and
            stage_seven_progress.token_command_line and
            stage_seven_progress.file_knowledge and
            stage_seven_progress.security_shield and
            stage_seven_progress.settings_key and
            stage_seven_progress.optimization_badge
        )

    # Определяем доступность этапов
    stage_access = [False] * 7  # Список для этапов 1–7 (индексы 0–6)
    stage_access[0] = True  # Этап 1 всегда доступен

    # Проверяем доступность этапов 2–6
    for i in range(1, total_stages):  # Индексы 1–5 (Этапы 2–6)
        previous_stage_completed = False
        for stat in all_results_sorted:
            if stat.step == i:  # Проверяем предыдущий этап (i+1 — текущий этап)
                if stat.total_questions:
                    previous_stage_completed = stat.score == stat.total_questions
                else:
                    previous_stage_completed = stat.score == 1
                break
        stage_access[i] = previous_stage_completed

    # Проверяем доступность Этапа 7
    stage_six_completed = False
    for stat in all_results_sorted:
        if stat.step == 6:
            if stat.total_questions:
                stage_six_completed = stat.score == stat.total_questions
            else:
                stage_six_completed = stat.score == 1
            break
    stage_access[6] = stage_six_completed

    context = {
        'all_results': all_results_sorted,
        'awards': awards,  # Награды для этапов 1–6
        'stage_seven_completed': stage_seven_completed,  # Статус 7-го этапа
        'stage_access': stage_access,  # Доступность этапов
    }
    return render(request, 'accounts/map.html', context)

def stage_one_main(request):
    return render(request, 'accounts/stage_one/stage_one_main.html')


def stage_one_task(request):
    return render(request, 'accounts/stage_one/stage_one_task.html')


def stage_three_main(request):
    return render(request, 'accounts/stage_three/stage_three_main.html')


def terminal_view(request):
    output = ""
    command = ""
    # Симулируем начальное положение "директории"
    current_dir = "/"

    if request.method == 'POST':
        command = request.POST.get('command', '').strip()

        # Обработка базовых команд
        if command == "pwd":
            output = current_dir
        elif command == "ls":
            # Примерный список каталогов
            output = "home  var  usr"
        elif command.startswith("cd "):
            # Извлекаем путь после "cd "
            path = command[3:].strip()
            if path == "/home/student":
                current_dir = path
                output = f"Перешли в {current_dir}"
            else:
                output = f"Нет такого каталога: {path}"
        else:
            output = "Неизвестная команда"

    context = {
        "output": output,
        "command": command
    }

    return render(request, 'accounts/stage_two/terminal.html', context)


@login_required
@csrf_exempt
def save_quiz_result(request):
    # Первый квест!
    # TODO: Возможность, сохранение наилучшего результата только!
    if request.method == "POST":
        data = json.loads(request.body)
        user = request.user
        score = data.get("score")
        step = data.get('step')
        total_questions = data.get("total_questions")

        if QuizResult.objects.filter(user=user, step=step).exists():
            quiz_result = QuizResult.objects.filter(user=user, step=step).first()
            quiz_result.score = score
            quiz_result.step = step
            quiz_result.total_questions = total_questions

            quiz_result.save()
            message = "Результат обновлён"
        else:
            QuizResult.objects.create(
                user=user,
                step=step,
                score=score,
                total_questions=total_questions
            )

        return JsonResponse({"message": 'message', "status": "success"})


@login_required
@csrf_exempt
def save_quiz_result_two(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user = request.user
        completed = data.get('completed')
        step = data.get('step')

        if QuizResult.objects.filter(user=user, step=step).exists():
            quiz_result = QuizResult.objects.filter(user=user, step=step).first()
            quiz_result.score = completed
            quiz_result.save()
            message = "Результат обновлён"
        else:
            QuizResult.objects.create(
                user=user,
                step=step,
                score=completed,
            )
            message = "Результат сохранён"

        return JsonResponse({"message": message, "status": "success"})


@login_required
@csrf_exempt
def save_quiz_result_five(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user = request.user
        completed = data.get('completed')
        step = data.get('step')

        if QuizResult.objects.filter(user=user, step=step).exists():
            quiz_result = QuizResult.objects.filter(user=user, step=step).first()
            quiz_result.score = completed
            quiz_result.save()
            message = "Результат обновлён"
        else:
            QuizResult.objects.create(
                user=user,
                step=step,
                score=completed
            )
            message = "Результат сохранён"

        return JsonResponse({"message": message, "status": "success"})

@login_required
@require_POST
def save_progress(request):
    try:
        data = json.loads(request.body)
        task_name = data.get('task_name')
        completed = data.get('completed', False)

        # Получаем или создаем запись прогресса для текущего пользователя
        progress, created = StageSevenProgress.objects.get_or_create(user=request.user)

        # Названия полей в модели StageSevenProgress
        task_field_map = {
            "Бейджик Инициации": "badge_initiation",
            "Токен Командной Строки": "token_command_line",
            "Файл Знаний": "file_knowledge",
            "Щит Безопасности": "security_shield",
            "Ключ Настройки": "settings_key",
            "Оптимизирующий Бейдж": "optimization_badge"
        }

        # Проверяем, существует ли поле для этого задания
        if task_name in task_field_map:
            field_name = task_field_map[task_name]
            setattr(progress, field_name, completed)
            progress.save()
            return JsonResponse({'status': 'success', 'message': 'Progress saved'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid task name'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@login_required
def get_progress(request):
    try:
        # Получаем прогресс текущего пользователя
        progress, created = StageSevenProgress.objects.get_or_create(user=request.user)
        progress_dict = {
            "Бейджик Инициации": progress.badge_initiation,
            "Токен Командной Строки": progress.token_command_line,
            "Файл Знаний": progress.file_knowledge,
            "Щит Безопасности": progress.security_shield,
            "Ключ Настройки": progress.settings_key,
            "Оптимизирующий Бейдж": progress.optimization_badge
        }
        return JsonResponse({'status': 'success', 'progress': progress_dict})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
def stage_four(request):
    return render(request, 'accounts/stage_four/index.html')


def stage_five_main(request):
    return render(request, 'accounts/stage_five/stage_five_main.html')


def stage_six(request):
    return render(request, 'accounts/stage_six/index.html')


def stage_seven(request):
    return render(request, 'accounts/stage_seven/main.html')


def stage_seven_terminal(request):
    return render(request, 'accounts/stage_seven/stage_seven_terminal.html')


def stage_seven_conf(request):
    return render(request, 'accounts/stage_seven/stage_seven_conf.html')
