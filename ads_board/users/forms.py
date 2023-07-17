from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.transaction import commit
from django.shortcuts import reverse


class RegistrationForm(UserCreationForm):
    """
    A form for user registration, extending the UserCreationForm provided by Django.
    It adds an email field to the form.
    """

    email = forms.CharField(label='Email', max_length=254,
                            help_text='Обязательное поле. Введите действующий адрес электронной почты.')

    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2')

    def save(self, commit=True):
        """
        Save the user instance after registration.
        If commit is True, the user is saved to the database.
        Returns the saved user instance.
        """
        user = super().save(commit=False)
        if commit:
            user.save()
        return user


class CustomRegistrationForm(RegistrationForm):
    """
    A custom registration form that extends the RegistrationForm.
    It adds functionality to store a redirect URL in the session after saving the user.
    """

    def save(self, request):
        """
        Save the user instance and store a redirect URL in the session.
        If commit is True, the user is saved to the database.
        Returns the saved user instance.
        """
        user = super().save(commit=False)
        if commit:
            user.save()

        redirect_url = reverse('ads:advert-list')
        request.session['redirect_url'] = redirect_url

        return user


class LoginForm(forms.Form):
    """
    A form for user login.
    It includes fields for username and password.
    """

    username = forms.CharField(label='Имя пользователя', max_length=254)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
