from datetime import timedelta
from django.utils import timezone
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.contrib.auth.models import User
from celery import shared_task

from ads.models import Advert
from ads_board import settings


@shared_task
def send_email():
    """
    Celery task to send weekly email with new adverts to all registered users.
    """
    today = timezone.now()
    last_week = today - timedelta(days=7)

    # Get all adverts created in the last week
    adverts = Advert.objects.filter(created_at__gte=last_week)

    # Get all registered users
    users = User.objects.all()

    for user in users:
        # Get the email address of the user
        email = user.email

        # Generate HTML content for the email, passing the adverts and the site link
        html_content = render_to_string(
            'daily_advert.html',
            {
                'adverts': adverts,
                'link': settings.SITE_URL,
            }
        )

        # Create an EmailMultiAlternatives object for sending the email
        msg = EmailMultiAlternatives(
            subject='Weekly Adverts',
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email],
        )

        # Attach the HTML content to the email
        msg.attach_alternative(html_content, 'text/html')

        # Send the email to the user
        msg.send()
