from django.utils import timezone

from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from ads.models import Advert, Category
from ads_board import settings


# рассылка подписчикам списка публикаций за неделю
# через celery.py/app.conf.beat_schedule
@shared_task
def send_email():
    today = timezone.now()
    last_week = today - timezone.timedelta(days=7)
    posts = Advert.objects.filter(date__gte=last_week)
    categories = set(posts.values_list('category__name', flat=True))
    subscribers = set(Category.objects.filter(name__in=categories).values_list('subscribers__email', flat=True))
    html_content = render_to_string(
        'daily_advert.html',
        {
            'link': settings.SITE_URL,
            'advert': advert,
        }
    )
    msg = EmailMultiAlternatives(
        subject='Статьи за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()

