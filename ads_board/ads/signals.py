from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

from ads.models import Response


@receiver(post_save, sender=Response)
def response_created(instance, created, **kwargs):
    if created:
        send_mail(
            subject='На ваше объявление откликнулись!',
            message=f'{instance.advert.user.username}, вам оклик от {instance.user.username}! Вот он: "{instance.response_text}" ',
            from_email=None,
            recipient_list=[instance.advert.user.email],
        )
        return


@receiver(post_save, sender=Response)
def response_accept(instance, **kwargs):
    if instance.status:
        send_mail(
            subject='Ваш отклик приняли!',
            message=f'{instance.author.username}, ваш отклик к {instance.advert.title} приняли',
            from_email=None,
            recipient_list=[instance.author.email],
        )
        return
