from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.transaction import commit
from django.shortcuts import reverse

from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from django.core.mail import EmailMultiAlternatives
from django.core.mail import mail_admins

from ads_board import settings


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


class CustomRegistrationForm(RegistrationForm):
    def save(self, request):
        user = super().save(commit=False)
        if commit:
            user.save()

        # Добавьте здесь логику перенаправления на страницу со списком объявлений
        redirect_url = reverse('ads:advert-list')  # Замените 'ads:advert-list' на URL-шаблон списка объявлений
        request.session['redirect_url'] = redirect_url

        return user


def add_to_common_group(user):
    group = Group.objects.get(name='Пользователи')
    group.user_set.add(user)


class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        basic_group = Group.objects.get(name='Пользователи')
        basic_group.user_set.add(user)

        subject = 'Добро пожаловать на наш сайт объявлений!'
        text = f'{user.username}, вы успешно зарегистрировались на сайте!'
        html = (
            f'<b>{user.username}</b>, вы успешно зарегистрировались на '
            f'<a href="http://127.0.0.1:8000/">сайте</a>!'
        )
        msg = EmailMultiAlternatives(
            subject=subject,
            body=text,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email]
        )
        msg.attach_alternative(html, "text/html")
        msg.send()

        mail_admins(
            subject='Новый пользователь!',
            message=f'Пользователь {user.username} зарегистрировался на сайте.'
        )
        return user
