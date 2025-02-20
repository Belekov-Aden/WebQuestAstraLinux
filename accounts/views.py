import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
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
    # Login admin: root
    # Password: admin: root
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


def map(request):
    return render(request, 'accounts/map.html')


def stage_one_main(request):
    return render(request, 'accounts/stage_one/stage_one_main.html')


def stage_one_task(request):
    return render(request, 'accounts/stage_one/stage_one_task.html')


@login_required
@csrf_exempt
def save_quiz_result(request):
    # Первый квест!
    if request.method == "POST":
        data = json.loads(request.body)
        user = request.user
        score = data.get("score")
        step = data.get('step')
        total_questions = data.get("total_questions")

        quiz_result, created = QuizResult.objects.update_or_create(
            user=user,
            step=step,
            defaults={
                'score': score,
                'total_questions': total_questions
            }
        )

        if created:
            message = "Результат сохранён"
        else:
            message = "Результат обновлён"

        return JsonResponse({"message": message, "status": "success"})
