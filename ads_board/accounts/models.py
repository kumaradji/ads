"""
Данный код представляет модель пользователя `CustomUser`, основанную на `AbstractBaseUser`.
В ней определены поля, такие как `email`, `username` и флаги `is_active`, `is_verified`, `is_admin`, `is_staff`.
Также есть поле `subscribed_categories`, которое представляет множество категорий, на которые пользователь подписан.
Модель `CustomUser` также содержит менеджер пользователей `CustomUserManager`, который отвечает за создание и
сохранение пользователей. В нем определены методы `create_user` и `create_superuser` для создания обычного
пользователя и суперпользователя соответственно.
Для регистрации пользователя на сайте на основе данной модели, вам необходимо выполнить следующие шаги:

1. Создайте форму для регистрации пользователя. Эта форма должна содержать поля, такие как `email`, `username`,
`password`, и другие необходимые поля, которые вы хотите включить. Например:

   ```python
   from django import forms

   class RegistrationForm(forms.Form):
       email = forms.EmailField()
       username = forms.CharField(max_length=30)
       password = forms.CharField(widget=forms.PasswordInput())
   ```

2. Создайте представление, которое будет обрабатывать отправку данных формы и создавать нового пользователя.
В этом представлении вы будете использовать метод `create_user` из `CustomUserManager` для создания пользователя.
Пример представления:

   ```python
   from django.shortcuts import render, redirect
   from .models import CustomUser

   def registration_view(request):
       if request.method == 'POST':
           form = RegistrationForm(request.POST)
           if form.is_valid():
               email = form.cleaned_data['email']
               username = form.cleaned_data['username']
               password = form.cleaned_data['password']

               # Создание нового пользователя
               user = CustomUser.objects.create_user(email=email, username=username, password=password)

               # Дополнительные действия, например, отправка подтверждения по электронной почте

               return redirect('registration_success')  # Перенаправление на страницу успешной регистрации
       else:
           form = RegistrationForm()

       return render(request, 'registration.html', {'form': form})
   ```

3. Создайте соответствующий шаблон `registration.html`, который будет содержать форму для регистрации пользователя.
Например:

   ```html
   <form method="post">
       {% csrf_token %}
       {{ form.as_p }}
       <button type="submit">Register</button>
   </form>
   ```

4. Настройте URL-шаблон, который будет связывать представление с URL-адресом. Например:

   ```python
   from django.urls import path
   from .views import registration_view

   urlpatterns = [
       path('register/', registration_view, name='registration'),
       # Другие URL-шаблоны вашего приложения
   ]
   ```
После выполнения этих шагов вы сможете использовать форму регистрации и представление для создания новых
 пользователей на вашем сайте.
"""


from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Модель `CustomUserManager` отвечает за создание и сохранение
# пользователей. В модели мы определяем несколько полей, таких как
# `email`, `username`, `is_active`, `is_admin`, `is_staff`.
# Мы также определяем необходимые методы для работы с пользователями,
# такие как `create_user`, `create_superuser`
class CustomUserManager(BaseUserManager):
    # Создает пользователя без прав администратора, проверяя наличие
    # обязательных полей email и username. Затем она нормализует email,
    # создает и сохраняет пользователя с указанными данными.
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Email address is required.")
        if not username:
            raise ValueError("Username is required.")

        email = self.normalize_email(email)
        user = self.model(email=email, username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    # Создает суперпользователя с правами администратора. Она вызывает
    # функцию create_user для создания пользователя с указанными данными
    # и затем устанавливает флаги is_admin и is_staff в значение True,
    # чтобы указать, что пользователь является администратором.
    # После этого суперпользователь сохраняется.
    def create_superuser(self, email, username, password=None):
        user = self.create_user(email=email, username=username, password=password)
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


# Модель `CustomUser` на основе `AbstractBaseUser`.
class CustomUser(AbstractBaseUser):
    # Поле электронной почты пользователя
    email = models.EmailField(verbose_name="Email address", max_length=255, unique=True)
    # Имя пользователя
    username = models.CharField(verbose_name="Username", max_length=30, unique=True)
    # Флаг, указывающий, активен ли пользователь
    is_active = models.BooleanField(default=True)
    # Флаг, указывающий, авторизовался ли пользователь
    is_verified = models.BooleanField(default=False)
    # Флаг, указывающий, является ли пользователь администратором
    is_admin = models.BooleanField(default=False)
    # Флаг, указывающий, имеет ли пользователь доступ к административным функциям
    is_staff = models.BooleanField(default=False)
    # Множество категорий, на которые пользователь подписан
    subscribed_categories = models.ManyToManyField('ads.Category', related_name='subscribers', blank=True)

    # Менеджер пользователей
    objects = CustomUserManager()

    # Поле, используемое для аутентификации пользователя (электронная почта)
    USERNAME_FIELD = 'email'
    # Дополнительные поля, требуемые при создании суперпользователя
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        # Возвращает имя пользователя в качестве строки представления объекта
        return self.username

    def has_perm(self, perm, obj=None):
        # Проверяет, имеет ли пользователь указанные разрешения
        # В данном случае, администратор всегда имеет все разрешения
        return self.is_admin

    def has_module_perms(self, app_label):
        # Проверяет, имеет ли пользователь разрешения для данного модуля (приложения)
        # В данном случае, администратор всегда имеет разрешения для всех модулей
        return self.is_admin

    def subscribe_to_category(self, category):
        # Подписывает пользователя на указанную категорию
        self.subscribed_categories.add(category)

    def unsubscribe_from_category(self, category):
        # Отписывает пользователя от указанной категории
        self.subscribed_categories.remove(category)

    def get_subscribed_categories(self):
        # Возвращает список категорий, на которые пользователь подписан
        return self.subscribed_categories.all()


