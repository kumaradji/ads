from django.contrib.auth import login, authenticate, get_user_model, models
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.views import LogoutView
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.views.generic import ListView, DeleteView
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView
from django.core.mail import send_mail

from .forms import RegistrationForm, LoginForm
from ads.models import Response, Advert
import random
import string

from .models import Profile


def generate_confirmation_code():
    """Генерирует случайный код подтверждения."""
    code_length = 6
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(code_length))


class SignUp(CreateView):
    model = get_user_model()
    form_class = RegistrationForm
    template_name = 'users/signup.html'
    success_url = reverse_lazy('ads:advert-list')

    def form_valid(self, form):
        user = form.save()
        group = Group.objects.get_or_create(name='Пользователи')[0]
        user.groups.add(group)
        user.save()

        confirmation_code = generate_confirmation_code()

        # Генерируем HTML-контент для письма
        html_content = render_to_string('users/registration_email.html', {
            'username': user.username,
            'confirmation_code': confirmation_code,
        })

        # Отправляем письмо с кодом подтверждения и приветственным сообщением
        send_mail(
            subject='Добро пожаловать на наш сайт объявлений!',
            message='',
            from_email=None,
            recipient_list=[user.email],
            html_message=html_content
        )

        return redirect('users:confirmation')


class ConfirmationView(View):
    template_name = 'users/confirmation.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        return redirect('users:login')


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'users/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            if username and password:
                user = authenticate(request, username=username, password=password)

                if user is not None and user.is_active:
                    login(request, user)
                    next_url = request.GET.get('next')
                    if next_url:
                        return redirect(next_url)
                    else:
                        return redirect('advert-list')
        else:
            form.add_error(None, 'Неверные имя пользователя или пароль.')
        return render(request, 'users/login.html', {'form': form})


class LogoutView(LogoutView):
    next_page = 'users:login'


class ResponseListView(LoginRequiredMixin, ListView):
    template_name = 'users/response_list.html'
    context_object_name = 'responses'

    def get_queryset(self):
        return Response.objects.filter(author=self.request.user)


class ResponseDeleteView(LoginRequiredMixin, DeleteView):
    model = Response
    template_name = 'users/response_confirm_delete.html'
    success_url = reverse_lazy('profile')

    def get_queryset(self):
        user = self.request.user
        return Response.objects.filter(article__user=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article'] = self.object.article
        return context

    def post(self, request, *args, **kwargs):
        response = self.get_object()
        if 'delete' in request.POST:
            response.delete()
        elif 'accept' in request.POST:
            response.like()
        elif 'reject' in request.POST:
            response.dislike()
        return redirect('profile')


class PrivateProfileView(LoginRequiredMixin, View):
    template_name = 'ads/private_page.html'

    def get(self, request):
        user = request.user
        adverts = Advert.objects.filter(user=user)
        responses = Response.objects.filter(advert__user=user)
        is_author = Profile.objects.filter(user=user, is_author=True).exists()

        context = {
            'user': user,
            'adverts': adverts,
            'responses': responses,
            'is_author': is_author,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        user = request.user
        is_author = False

        if not Profile.objects.filter(user=user, is_author=True).exists():
            author_group = Group.objects.get_or_create(name='Авторы')[0]
            user.groups.add(author_group)
            user.save()
            is_author = True

        adverts = Advert.objects.filter(user=user)
        responses = Response.objects.filter(advert__user=user)

        context = {
            'user': user,
            'adverts': adverts,
            'responses': responses,
            'is_author': is_author,
        }
        return render(request, self.template_name, context)


@login_required
def profile(request):
    return redirect('ads:private')
