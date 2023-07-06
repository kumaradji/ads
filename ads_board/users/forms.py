from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.transaction import commit
from django.shortcuts import reverse


class RegistrationForm(UserCreationForm):
    email = forms.CharField(label='Email', max_length=254,
                            help_text='Обязательное поле. Введите действующий адрес электронной почты.')

    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(label='Имя пользователя', max_length=254)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)


class CustomRegistrationForm(RegistrationForm):
    def save(self, request):
        user = super().save(commit=False)
        if commit:
            user.save()

        # Добавьте здесь логику перенаправления на страницу со списком объявлений
        redirect_url = reverse('ads:advert-list')  # Замените 'ads:advert-list' на URL-шаблон списка объявлений
        request.session['redirect_url'] = redirect_url

        return user
