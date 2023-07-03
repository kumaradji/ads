from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail

from accounts.models import CustomUser, Author


# Отправка сигнала когда появляется объявления в первый раз
@receiver(post_save, sender=CustomUser)
def my_handler(sender, instance, created, **kwargs):
    # Отправка сигнала если автор принял отклик
    if instance.status:
        mail = instance.author.email
        send_mail(
            'Subject here',
            'Here is the message.',
            'host@mail.ru',
            [mail],
            fail_silently=False,
        )
    # Отправка на почту автору объявления, если ещё отклик не принят
    mail = instance.article.author.email
    send_mail(
        'Subject here',
        'Here is the message.',
        'host@mail.ru',
        [mail],
        fail_silently=False,
    )


@receiver(post_save, sender=User)
def create_author(sender, instance, created, **kwargs):
    if created:
        Author.objects.create(user=instance)
