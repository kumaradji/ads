from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth import get_user_model


class CustomUserManager(BaseUserManager):
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


# Модель `CustomUser` на основе `AbstractBaseUser`.
class CustomUser(AbstractBaseUser):
    email = models.EmailField(verbose_name="Email address", max_length=255, unique=True)
    username = models.CharField(verbose_name="Username", max_length=30, unique=True)
    subscribed_categories = models.ManyToManyField('ads.Category', related_name='subscribers', blank=True)
    is_author = models.BooleanField(default=False)
    # Менеджер пользователей
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.username

