from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic.edit import CreateView

from .forms import RegistrationForm, LoginForm


class SignUp(CreateView):
    model = User
    form_class = RegistrationForm
    success_url = '/accounts/signup'
    template_name = 'accounts/signup.html'

    def form_valid(self, form):
        form.save()
        return redirect('profile')


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        # Здесь можно добавить логику для получения информации о профиле пользователя
        # Например:
        user = request.user
        context = {
            'user': user
        }
        return render(request, 'accounts/profile.html', context)


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
                return redirect('accounts:profile')
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

