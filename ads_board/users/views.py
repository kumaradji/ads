from django.contrib.auth import login, authenticate, get_user_model, models
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.views import LogoutView
from django.shortcuts import redirect, render
from django.views.generic import ListView, DeleteView
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic.edit import CreateView
from django.core.mail import send_mail

from .forms import RegistrationForm, LoginForm
from ads_board.tasks.tasks import send_registration_email
from ads.models import Response
import random
import string


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

        # Запланировать задачу отправки письма с помощью Celery
        send_registration_email.delay(user.email, confirmation_code)

        # Отправить письмо приветствия
        send_mail(
            subject='Добро пожаловать на наш сайт объявлений!',
            message=f'{user.username}, вы успешно зарегистрировались!',
            from_email=None,
            recipient_list=[user.email],
        )

        return redirect('users:confirmation')


class ConfirmationView(View):
    template_name = 'users/confirmation.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        return redirect('users:login')


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        context = {
            'user': user
        }
        return render(request, 'users/profile.html', context)

    def post(self, request):
        user = request.user

        if not user.is_staff:
            author_group = models.Group.objects.get(name='Авторы')
            user.groups.add(author_group)
            user.is_staff = True
            user.save()

        return redirect('profile')


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


@login_required
def profile(request):
    user = request.user

    if not user.groups.filter(name='Авторы').exists():
        author_group = Group.objects.get(name='Авторы')
        user.groups.add(author_group)
        user.is_author = True
        user.save()

    context = {
        'user': user
    }
    return render(request, 'users/profile.html', context)
