from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from ads.models import Response


@receiver(post_save, sender=Response)
def my_handler (sender, instance, created, **kwargs):
    if not instance.status == True:
        return
    mail = instance.article.author.email
    send_mail(
        'Subject here',
        'Here is the message.',
        'host@mail.ru',
        [mail],
        fail_silently=False,
    )

