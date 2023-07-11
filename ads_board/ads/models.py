from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Advert(models.Model):
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

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='advert')
    content = models.TextField(verbose_name="Content")
    title = models.CharField(verbose_name="Title", max_length=100)
    category = models.CharField(verbose_name="Category",
                                max_length=20,
                                choices=CATEGORY_CHOICES,
                                default='Tanks')
    response_text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    upload = models.FileField(upload_to='uploads/',
                              help_text='загрузите файл',
                              blank=True)

    def __str__(self):
        return self.title

    def preview(self):
        return self.content[0:120] + '...'

    def get_absolute_url(self):
        return f'/{self.id}'

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'


class Response(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE, related_name='authored_response')
    advert = models.ForeignKey(Advert, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='responses')
    article = models.ForeignKey(Advert,
                                on_delete=models.CASCADE,
                                related_name='responses')
    response_text = models.TextField(verbose_name='Response text')
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Created at')
    status = models.BooleanField(default=False,
                                 verbose_name='Is accepted')
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'Отклик от {self.user.username} на объявление: {self.article.title}'

    def accept(self):
        self.status = True
        self.save()

    def like(self):
        self.status = True
        self.save()

    def dislike(self):
        self.status = False
        self.save()

    class Meta:
        verbose_name = 'Отклик'
        verbose_name_plural = 'Отклики'


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Category Name")
    is_ad_category = models.BooleanField(default=False, verbose_name="Is Advertisement Category")
    adverts = models.ManyToManyField(Advert, related_name='categories', verbose_name="Adverts")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
