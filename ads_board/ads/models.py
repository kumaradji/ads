from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

User = get_user_model()


class Advert(models.Model):
    """
    Model representing an advertisement.
    """

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

    # User who created the advertisement (User model).
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='advert')
    # Content of the advertisement.
    content = models.TextField(verbose_name="Content")
    # Title of the advertisement.
    title = models.CharField(verbose_name="Title", max_length=100)
    # Category of the advertisement.
    category = models.CharField(
        verbose_name="Category",
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='Tanks'
    )
    # Text content of the response to the advertisement.
    response_text = models.TextField(blank=True)
    # Date and time of advertisement creation.
    created_at = models.DateTimeField(auto_now_add=True)
    # File upload field for the advertisement.
    upload = models.FileField(
        upload_to='uploads/',
        help_text='Upload a file',
        blank=True
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('ads:advert-detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Advertisement'
        verbose_name_plural = 'Advertisements'


class Response(models.Model):
    """
    Model representing a response to an advertisement.
    """

    # Author of the response (User model).
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='authored_responses')
    # Related advertisement (Advert model).
    advert = models.ForeignKey(Advert, on_delete=models.CASCADE)
    # User who made the response (User model).
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='responses')
    # Text content of the response.
    response_text = models.TextField(verbose_name='Response text')
    # Date and time of response creation.
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    # Response acceptance status.
    status = models.BooleanField(default=False, verbose_name='Is accepted')
    # Number of likes received by the response.
    likes = models.PositiveIntegerField(default=0)
    # Number of dislikes received by the response.
    dislikes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'Response from {self.user.username} to the advertisement: {self.advert.title}'

    def accept(self):
        """
        Mark the response as accepted.
        """
        self.status = True
        self.save()

    def like(self):
        """
        Increase the number of likes for the response.
        """
        self.status = True
        self.save()

    def dislike(self):
        """
        Increase the number of dislikes for the response.
        """
        self.status = False
        self.save()

    class Meta:
        permissions = [('response_create', 'Can create response')]
        verbose_name = 'Response'
        verbose_name_plural = 'Responses'

    def get_absolute_url(self):
        return reverse('ads:response-detail', kwargs={'pk': self.pk})


class Category(models.Model):
    """
    Model representing a category of advertisements.
    """

    # Name of the category.
    name = models.CharField(max_length=255, unique=True, verbose_name="Category Name")
    # Indicates if the category is an advertisement category.
    is_ad_category = models.BooleanField(default=False, verbose_name="Is Advertisement Category")
    # Many-to-many relationship field linking the category to the advertisements.
    adverts = models.ManyToManyField(Advert, related_name='categories', verbose_name="Adverts")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
