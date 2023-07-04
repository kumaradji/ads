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
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('profile')

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
        return render(request, 'accounts/profile.html', context)

    def post(self, request):
        User = get_user_model()
        user = request.user

        if not user.is_author:
            author_group = models.Group.objects.get(name='Авторы')
            user.groups.add(author_group)
            user.customuser.is_author = True
            user.customuser.save()

        return redirect('profile')


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'accounts/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile')
            form.add_error(None, 'Неверные имя пользователя или пароль.')
        return render(request, 'accounts/login.html', {'form': form})


class LogoutView(View):
    @login_required
    def get(self, request):
        logout(request)
        return redirect('accounts:login')

    def post(self, request):
        logout(request)
        return redirect('accounts:login')


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
    return render(request, 'accounts/profile.html', context)
