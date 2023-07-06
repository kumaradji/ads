from allauth.account.forms import LoginForm
from django.contrib.auth import login, logout, authenticate, get_user_model, models
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group, User
from django.contrib.auth.views import LogoutView
from django.shortcuts import redirect, render
from django.views.generic import ListView, DeleteView
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic.edit import CreateView
from users.models import CustomUser

from ads.models import Advert, Response

from django.views.generic.edit import CreateView
from .forms import CustomSignupForm


class SignUp(CreateView):
    model = User
    form_class = CustomSignupForm
    success_url = '/accounts/login'
    template_name = 'registration/signup.html'


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


# class LoginView(View):
#     def get(self, request):
#         form = LoginForm()
#         return render(request, 'users/login.html', {'form': form})
#
#     def post(self, request):
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             print(f"Username: {username}")  # Отладочный вывод
#             print(f"Password: {password}")  # Отладочный вывод
#             if username and password:
#                 user = authenticate(request, username=username, password=password)
#                 print("User authentication successful")  # Отладочный вывод
#
#                 if user is not None and user.is_active:
#                     print("User authentication successful")  # Отладочный вывод
#                     login(request, user)
#                     next_url = request.GET.get('next')
#                     if next_url:
#                         print(f"Redirecting to next URL: {next_url}")  # Отладочный вывод
#                         return redirect(next_url)
#                     else:
#                         return redirect(reverse('profile'))
#         else:
#             print("Form is invalid")  # Отладочный вывод
#         form.add_error(None, 'Неверные имя пользователя или пароль.')
#         return render(request, 'users/login.html', {'form': form})


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
