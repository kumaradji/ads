from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, User


# Модель, содержащая объекты всех авторов
class Author(models.Model):
    # связь «один к одному» с встроенной моделью пользователей User;
    author = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'

    #  функция, которая говорит, как лучше вывести объект в админ панель
    def __str__(self):
        return f'{self.authorUser}'


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
