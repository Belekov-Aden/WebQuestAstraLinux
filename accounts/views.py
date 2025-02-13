from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import RegisterUserForm


def register(request):
    if request.method == 'POST':
        user_form = RegisterUserForm(request.POST)

        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password1'])
            new_user.save()
            return render(request, 'accounts/register_done.html')

    else:
        user_form = RegisterUserForm()
        return render(request, 'accounts/register.html', {'form': user_form})



def login(request):
    ...