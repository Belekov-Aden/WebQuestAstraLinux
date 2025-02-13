from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import forms


class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def clean_password2(self):
        cd = self.cleaned_data

        if cd['password1'] != cd['password2']:
            raise forms.ValidationError("Password dont match")
        return cd["password2"]


class LoginUserForm(AuthenticationForm):
    ...
