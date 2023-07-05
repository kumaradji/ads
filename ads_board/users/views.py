from django.contrib.auth import login, logout, authenticate, get_user_model, models
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic.edit import CreateView

from .forms import RegistrationForm, LoginForm


class SignUp(CreateView):
    model = get_user_model()
    form_class = RegistrationForm
    template_name = 'users/signup.html'
    success_url = '/users/profile/'

    def form_valid(self, form):
        user = form.save()
        group = Group.objects.get_or_create(name='Пользователи')[0]
        user.groups.add(group)  # добавляем нового пользователя в эту группу
        user.save()
        return super().form_valid(form)


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
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_staff:
                login(request, user)
                return redirect(reverse('profile'))  # Изменяем перенаправление на URL-шаблон 'profile'
            form.add_error(None, 'Неверные имя пользователя или пароль.')
        return render(request, 'users/login.html', {'form': form})  # Возвращаем шаблон login.html при ошибке


class LogoutView(View):
    @login_required
    def get(self, request):
        logout(request)
        return redirect('users:login')

    def post(self, request):
        logout(request)
        return redirect('users:login')


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
