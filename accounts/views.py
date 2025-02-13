from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import RegisterUserForm, LoginForm


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
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponse(f'Hello {request.user.username}')
            else:
                form.add_error(None, "Неверное имя пользователя или пароль")
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')  # После выхода перенаправляем на страницу входа
