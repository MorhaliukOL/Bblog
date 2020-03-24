import os
from celery import shared_task
from django.core.mail import send_mail
from dotenv import load_dotenv

load_dotenv()


@shared_task
def send_email_task(author, post_url, emails):
    send_mail(
        f'{author} has just published a new post',
        post_url,
        os.getenv('EMAIL_HOST_USER'),
        emails,
    )
