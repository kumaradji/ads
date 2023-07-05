from django.contrib.auth.models import User
from django.db import models

from users.models import CustomUser
from ads_board import settings


class Advert(models.Model):

    # Выборы категории: (значение, отображаемый текст)
    CATEGORY_CHOICES = [
        ('Tanks', 'Танки'),
        ('Healers', 'Хилы'),
        ('DD', 'ДД'),
        ('Merchants', 'Торговцы'),
        ('Guild Masters', 'Гилдмастеры'),
        ('Quest Givers', 'Квестгиверы'),
        ('Smiths', 'Кузнецы'),
        ('Tanner', 'Кожевники'),
        ('Potion', 'Зельевары'),
        ('Spellmasters', 'Мастера заклинаний'),
    ]

    # Внешний ключ, связывающий объявление с пользователем
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='advert')
    # Поле для содержания и текста объявления
    content = models.TextField(verbose_name="Content")
    # Поле для заголовка объявления
    title = models.CharField(verbose_name="Title", max_length=100)
    # Поле для выбора категории из предопределенных вариантов
    category = models.CharField(verbose_name="Category",
                                max_length=20,
                                choices=CATEGORY_CHOICES,
                                default='Tanks')
    # Поле для содержания текста отклика
    response_text = models.TextField(blank=True)
    # Поле для хранения даты и времени создания объявления
    created_at = models.DateTimeField(auto_now_add=True)
    # Поле указывающее куда загружать контент видео или картинку
    upload = models.FileField(upload_to='uploads/',
                              help_text='загрузите файл',
                              blank=True)

    def __str__(self):
        return self.title

    # превью объявления, мы взяли часть текста (первые 120 символа) и прибавили многоточие в конце
    def preview(self):
        return self.content[0:120] + '...'

    # добавим абсолютный путь, чтобы после создания нас перебрасывало на страницу со списком объявлений
    def get_absolute_url(self):
        return f'/{self.id}'

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'


class Response(models.Model):
    # Поле для имени автора отклика
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    # Внешний ключ, связывающий отклик с пользователем
    user = models.ForeignKey(CustomUser,
                             on_delete=models.CASCADE,
                             related_name='responses',
                             verbose_name='User')
    # Внешний ключ, связывающий отклик с объявлением
    article = models.ForeignKey(Advert,
                                on_delete=models.CASCADE,
                                related_name='responses',
                                verbose_name='Article')
    # Поле для содержания текста отклика
    response_text = models.TextField(verbose_name='Response text')
    # Поле для хранения даты и времени создания отклика
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Created at')
    # Поле, указывающее, был ли отклик принят
    status = models.BooleanField(default=False,
                                 verbose_name='Is accepted')

    def __str__(self):
        # Возвращает строковое представление отклика
        return f'Отклик от {self.user.username} на объявление: {self.article.title}'

    def like(self):
        # Фиксирует лайк на отклике
        self.is_accepted = True
        self.save()

    def dislike(self):
        # Фиксирует дизлайк на отклике
        self.is_accepted = False
        self.save()

    class Meta:
        verbose_name = 'Отклик'
        verbose_name_plural = 'Отклики'


class Category(models.Model):
    """
    Model representing a category.
    """

    name = models.CharField(max_length=255, unique=True, verbose_name="Category Name")
    is_ad_category = models.BooleanField(default=False, verbose_name="Is Advertisement Category")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

