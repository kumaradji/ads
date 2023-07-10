from datetime import timedelta
from ads_board.celery import app as celery_app

__all__ = ('celery_app',)

from celery import shared_task
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.core.mail import send_mail

from ads.models import Advert, Category
from ads_board import settings


@shared_task
def send_registration_email(email, confirmation_code):
    subject = 'Подтверждение регистрации'
    message = f'Ваш код подтверждения: {confirmation_code}'
    from_email = 'Ku79313081435@yandex.ru'
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list)


@shared_task
def send_email():
    today = timezone.now()
    last_week = today - timedelta(days=7)
    adverts = Advert.objects.filter(created_at__gte=last_week)
    subscribers = Category.objects.filter(adverts__in=adverts).values_list('subscribers__email', flat=True).distinct()

    html_content = render_to_string(
        'daily_advert.html',
        {
            'adverts': adverts,
            'link': settings.SITE_URL,
        }
    )
    msg = EmailMultiAlternatives(
        subject='Объявления за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
