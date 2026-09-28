from celery import shared_task

from task.models import Task
from .services import (
    send_web_activation_email,
    send_activation_email,
    send_reset_password_email,
)
from .models import User
from datetime import timedelta
from django.utils import timezone


@shared_task(
    autoretry_for=(ConnectionError,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 5},
)
def send_web_activation_email_task(token, user_id):
    user = User.objects.get(pk=user_id)
    send_web_activation_email(user, token)


@shared_task(
    autoretry_for=(ConnectionError,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 5},
)
def send_activation_email_task(token, user_id):
    user = User.objects.get(pk=user_id)
    send_activation_email(user, token)


@shared_task(
    autoretry_for=(ConnectionError,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 5},
)
def send_reset_password_email_task(token, user_id):
    user = User.objects.get(pk=user_id)
    send_reset_password_email(user, token)


@shared_task(
    autoretry_for=(ConnectionError,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 5},
)
def delete_old_done_task():
    Task.objects.filter(
        done=True, updated_at__lt=timezone.now() - timedelta(days=1)
    ).delete()
