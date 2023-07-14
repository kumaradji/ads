from datetime import timedelta
from django.utils import timezone
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from celery import shared_task
from django.contrib.auth.models import User
from django.core.mail import send_mail

from ads.models import Advert
from ads_board import settings


@shared_task
def send_email():
    today = timezone.now()
    last_week = today - timedelta(days=7)
    adverts = Advert.objects.filter(created_at__gte=last_week)

    # Получаем всех зарегистрированных пользователей
    users = User.objects.all()

    for user in users:
        # Получаем адрес электронной почты пользователя
        email = user.email

        # Генерируем HTML-контент для письма, передавая объявления и ссылку на сайт
        html_content = render_to_string(
            'daily_advert.html',
            {
                'adverts': adverts,
                'link': settings.SITE_URL,
            }
        )

        # Создаем объект EmailMultiAlternatives для отправки писем
        msg = EmailMultiAlternatives(
            subject='Объявления за неделю',
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email],
        )

        # Прикрепляем HTML-контент к письму
        msg.attach_alternative(html_content, 'text/html')

        # Отправляем письмо пользователю
        msg.send()
