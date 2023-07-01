"""
Модели определяют поля и отношения между объектами данных, а представления
определяют логику обработки запросов и отображения данных.
В модели Advert определены поля для заголовка, содержания, категории, даты создания,
а также для хранения изображения и видео. Связь с пользователем установлена через внешний ключ user.
Модель News содержит поля для заголовка, текста и даты публикации новости.
Также есть дополнительные поля и методы, связанные с новостными рассылками.
Модель Response связывает отклик с пользователем и объявлением.
Она содержит поле для содержания отклика, даты создания и флага, указывающего, был ли отклик принят.
Модель Category определяет поля для названия категории и флага, указывающего,
является ли категория категорией объявлений.
Модель Newsletter содержит поля для заголовка, содержания, категорий и даты создания рассылки.
"""
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.models import CustomUser


class Advert(models.Model):
    """
    Model representing an advertisement.

    Attributes:
        CATEGORY_CHOICES (list): Choices for the category field.
        author (OneToOneField): One-to-one relationship with the User model
        representing the author of the advertisement.
        user (ForeignKey): Foreign key relationship with the CustomUser model
        representing the user associated with the advertisement.
        content (TextField): Text content of the advertisement.
        title (CharField): Title of the advertisement.
        category (CharField): Category of the advertisement chosen from predefined choices.
        created_at (DateTimeField): Date and time of the advertisement creation.
        upload (FileField): File field indicating where to upload video or image content.

    Methods:
        __str__(): Returns a string representation of the advertisement.

    Meta:
        verbose_name (str): Singular name for the model in the admin interface.
        verbose_name_plural (str): Plural name for the model in the admin interface.
    """

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

    # Поле для имени автора объявления
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    # Внешний ключ, связывающий объявление с пользователем
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE,
                             related_name='advert')
    # Поле для содержания и текста объявления
    content = models.TextField(verbose_name="Content")
    # Поле для заголовка объявления
    title = models.CharField(verbose_name="Title", max_length=100)
    # Поле для выбора категории из предопределенных вариантов
    category = models.CharField(verbose_name="Category",
                                max_length=20,
                                choices=CATEGORY_CHOICES,
                                default='Tanks')
    response_text = models.TextField(blank=True)

    # Поле для хранения даты и времени создания объявления
    created_at = models.DateTimeField(auto_now_add=True)
    # Поле указывающее куда загружать контент видео или картинку
    upload = models.FileField(upload_to='uploads/',
                              help_text='загрузите файл',
                              blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Advert")
        verbose_name_plural = _("Adverts")


class Response(models.Model):
    """
    Model representing a response to an advertisement.

    Attributes:
        author (OneToOneField): One-to-one relationship with the User model representing the author of the response.
        user (ForeignKey): Foreign key relationship with the CustomUser model representing the user associated with the response.
        article (ForeignKey): Foreign key relationship with the Advert model representing the advertisement the response is for.
        response_text (TextField): Text content of the response.
        created_at (DateTimeField): Date and time of the response creation.
        status (BooleanField): Indicates whether the response is accepted or not.

    Methods:
        __str__(): Returns a string representation of the response.
        like(): Sets the response as accepted (liked).
        dislike(): Sets the response as not accepted (disliked).

    Meta:
        verbose_name (str): Singular name for the model in the admin interface.
        verbose_name_plural (str): Plural name for the model in the admin interface.
    """

    # Поле для имени автора отклика
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    # Внешний ключ, связывающий отклик с пользователем
    user = models.ForeignKey(CustomUser,
                             on_delete=models.CASCADE,
                             related_name='responses',
                             verbose_name=_('User'))
    # Внешний ключ, связывающий отклик с объявлением
    article = models.ForeignKey(Advert,
                                on_delete=models.CASCADE,
                                related_name='responses',
                                verbose_name=_('Article'))
    # Поле для содержания текста отклика
    response_text = models.TextField(verbose_name=_('Response text'))
    # Поле для хранения даты и времени создания отклика
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_('Created at'))
    # Поле, указывающее, был ли отклик принят
    status = models.BooleanField(default=False,
                                 verbose_name=_('Is accepted'))

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
        verbose_name = _('Response')
        verbose_name_plural = _('Responses')


class Category(models.Model):
    """
    Model representing a category.
    """

    name = models.CharField(max_length=255, unique=True, verbose_name="Category Name")
    is_ad_category = models.BooleanField(default=False, verbose_name="Is Advertisement Category")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


def some_method(self):
    from accounts.models import CustomUser

    # Использование CustomUser здесь
    users = CustomUser.objects.all()
    pass
