from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from accounts.models import CustomUser


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254,
                             help_text='Обязательное поле. Введите действующий адрес электронной почты.')

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'password1', 'password2')


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Email', max_length=254)
